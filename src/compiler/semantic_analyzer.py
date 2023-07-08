import re

errors = []
funcName = ''
conditionalBlock = False
function_list = []

def reset():
    global errors
    global funcName
    global conditionalBlock
    global function_list
    errors = []
    funcName = ''
    conditionalBlock = False
    function_list = []

class FunctionInfo:
    def __init__(self, name, return_type, parameters):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.variables = {}
        self.variables_declaration = {} 
        self.body = [] 
        self.return_statement = []

    def display_info(self):
        print("Name: ", self.name)
        print("Return Type: ", self.return_type)
        print("Parameters:", self.parameters)
        print("Variables Types: ", self.variables)
        print("Variables Declaration: ", self.variables_declaration)
        print("Body:", self.body)
        print("Return Statement:", self.return_statement)

def addBodyFunctionInfo(funcName, variables):
    global conditionalBlock

    for func in function_list:
        if func.name == funcName:
            if conditionalBlock and ('condIf' in func.body[-1][0] or 'condElse' in func.body[-1][0]):
                func.body[-1].extend(variables)
            else:
                func.body.append(variables)
            break

def addReturnFunctionInfo(funcName, return_type):
    for func in function_list:
        if func.name == funcName:
            func.return_statement.append(return_type)
            break

def addVariableFunctionInfo(funcName, variables):
    for func in function_list:
        if func.name == funcName:
            v_type = variables[0]
            for variable in variables[1:]:
                func.variables[variable] = v_type
            break;
        
def addVariableDeclarationFunctionInfo(funcName, variables, line_num):
    for func in function_list:
        if func.name == funcName:
            v_type = variables[0]
            for variable in variables[1:]:
                func.variables[variable] = v_type
                func.variables_declaration[variable] = line_num
            break;

def addFunction(match):
    global funcName
    global function_list
    variables = re.findall(r'\b\w+\b', match[0])
    funcName = variables[1]
    f = FunctionInfo(variables[1], variables[0], variables[2:])
    function_list.append(f)

def addVariableDeclaration(match, line_num):
    global funcName
    variables = re.findall(r'\b\w+\b', match[0])
    addVariableDeclarationFunctionInfo(funcName, variables, line_num)


def addVariableDefinition(match, line_num):
    global funcName
    variables = re.findall(r'\b\d+\.\d+\b|\b\w+\b', match[0])

    if variables[0] in ['int','float']:
        addVariableDeclarationFunctionInfo(funcName, variables[:2], line_num)
        variables[1] = line_num + ' vdef ' + variables[1]
        addBodyFunctionInfo(funcName, variables[1:])
    else:
        variables[0] = line_num + ' vdef ' + variables[0]
        addBodyFunctionInfo(funcName, variables)

def addReturn(match):
    global funcName
    variables = re.findall(r'\b\w+\b', match[0])
    if re.match(r'\b\d+\b', variables[1]):
        if len(variables) > 2:
            variables[1] = 'value ' + variables[1]
            addReturnFunctionInfo(funcName, variables[1])
            variables[2] = 'value ' + variables[2]
            addReturnFunctionInfo(funcName, variables[2])
        else:
            variables[1] = 'value ' + variables[1]
            addReturnFunctionInfo(funcName, variables[1])
    else:
        variables[1] = 'v ' + variables[1]
        addReturnFunctionInfo(funcName, variables[1])

def addMain(match):
    global funcName
    global function_list
    variables = re.findall(r'\b\w+\b', match[0])
    funcName = variables[1]   
    f = FunctionInfo(variables[1], variables[0], variables[2:])
    function_list.append(f)

def addFunctionVariableAssignment(match):
    global funcName
    variables = re.findall(r'\b\w+\b', match[0])
    if variables[0] in ['int', 'float', 'string', 'char']:
        addVariableFunctionInfo(funcName, variables[:2])
    variables[0] = 'v ' + variables[0]
    variables[2] = 'fc ' + variables[2]
    addBodyFunctionInfo(funcName, variables)

def addIO(match, line_num):
    global funcName
    global function_list
    variables = re.findall(r'\b\w+\b', match[0])
    if len(variables) > 3 and 'n' in variables:
        variables.remove('n')
    variables[0] = line_num + ' io ' + variables[0]
    addBodyFunctionInfo(funcName, variables)

def addIfStatement(match, line_num):
    global funcName
    global function_list
    global conditionalBlock
    conditionalBlock = True
    variables = re.findall(r'\b\w+\b', match[0])
    variables[0] = line_num + ' condIf ' + variables[0]
    addBodyFunctionInfo(funcName, variables)

def addElseStatement(match, line_num):
    global funcName
    global function_list
    global conditionalBlock
    conditionalBlock = False
    variables = re.findall(r'\b\w+\b', match[0])
    variables[0] = line_num + ' condElse ' + variables[0]
    addBodyFunctionInfo(funcName, variables)
    conditionalBlock = True

def endOfConditional():
    global conditionalBlock
    conditionalBlock = False

def printFuncList():
    for function in function_list:
        function.display_info()
        print()

def checkVariableType(variable, aux_type):
    v_type = ''

    if aux_type == 'v' and re.match(r"\d+(?:\.\d+)?", variable):
        if '.' in variable:
            v_type = 'float'
        else:
            v_type = 'int'

    elif aux_type == 'v' and re.match(r'^.$', variable):
        v_type = 'char'

    elif aux_type == 'io' and variable in ['f','i']:
        if variable == 'f':
            v_type = 'float'
        elif variable == 'i':
            v_type = 'int'

    return v_type

def verify_return_of_operation(operation, func):
    aux_variables = {}
    for index, element in enumerate(operation):
        if element in ['float', 'int']:
            aux_variables[operation[index+1]] = element
        elif re.match(r'\b\d+\.\d+\b', element):
            aux_variables[element] = 'float'
        elif re.match(r'\b\d+\b', element):
            aux_variables[element] = 'int'
        else:
            if element in func.variables_declaration:
                aux_variables[element] = func.variables[element]

    for key, value in aux_variables.items():
        if value == 'float':
            return 'float'
    return 'int'

def verify_variables_of_operation(operation, func, variable, line_num):
    v_declaration_line = {}
    
    for element in operation:
        if element not in ['int', 'float'] and not re.match(r'\b\d+\.\d+\b', element) and not re.match(r'\b\d+\b', element):
            if element in func.variables_declaration:
                v_declaration_line[element] = func.variables_declaration[element]
    for key, value in v_declaration_line.items():
        if int(value) > int(line_num):
            errors.append(f'ERROR: Variable \'{key}\' in line \'{line_num}\' is not defined.')
            return False
    return True




def verify_variable_def(expression, func, line_num):
    global errors

    if isinstance(expression, str):
        if func.variables.get(expression) is None:
            errors.append(f'ERROR: Variable \'{expression}\' is not defined.')
            return

    elif isinstance(expression, list):
        _v = expression[0].split()[2]
        v_type = func.variables[_v]
        is_all_veriables_declared = verify_variables_of_operation(expression[1:], func, _v, line_num)
        if is_all_veriables_declared:
            operation_return = verify_return_of_operation(expression[1:], func)

            if v_type != operation_return:
                errors.append(f'ERROR: Variable \'{_v}\' expects {v_type} - Found \'{operation_return}\'.')
        return

def checkReturn(returnStatement, func):
    aux_type = returnStatement[0].split()[0]
    v = returnStatement[0].split()[1]
    if aux_type == 'v':
        v_return = func.variables[v]
        if func.return_type != v_return:
            errors.append(f'ERROR: \'{func.name}\' expects return {func.return_type} - Found \'{v_return}\'.')

    
def printErrors():
    for error in errors:
        print(error)

def semantic_analysis():
    # printFuncList()

    for func in function_list:
        ## verify all functions but main function
        if func.name != 'main':

            pass
            # for r in func.return_statement:
            #     found = False
            #
            #     ## verify if function return matches
            #     for index, p in enumerate(func.parameters):
            #         if r == p:
            #             found = True
            #             if func.parameters[index-1] != func.return_type:
            #                 errors.append(f'ERROR: In function \'{func.name}\' return does not match. Expected \'{func.return_type}\' - Found \'{func.parameters[index-1]}\'')
            #                 break
            #
            #     if not found:
            #         for index, b in enumerate(func.body):
            #             if r == b:
            #                 found = True
            #                 if func.body[index-1] != func.return_type:
            #                     errors.append(f'ERROR: In function \'{func.name}\' return does not match. Expected \'{func.return_type}\' - Founded \'{func.parameters[index-1]}\'')
            #                     break
            #
            #     if not found:
            #         errors.append(f'ERROR: In \'{func.name}\', \'{r}\' is not defined.')
        ## main function
        else:
            for index, b in enumerate(func.body):
                line_num = b[0].split()[0]
                aux_type = b[0].split()[1]

                if aux_type == 'vdef':
                    verify_variable_def(b, func, line_num)

                elif aux_type == 'condIf':
                    condition = b[1:3]
                    for exp in condition:
                        verify_variable_def(exp, func, line_num)

                    inicial_index = 3
                    exp = b[3:]
                    begin = 3
                    ## Verify expressions inside if 
                    for index, element in enumerate(b[4:]):
                        if len(element.split()) > 1:
                            verify_variable_def(exp[begin:index+1], func, line_num)
                            begin = index + 1

                    verify_variable_def(exp, func, line_num)

                elif aux_type == 'condElse':

                    verify_variable_def(b[1:], func, line_num)


                elif aux_type == 'io':

                    specifier = b[1]
                    v_type = checkVariableType(specifier, aux_type)
                    _v = b[2]
                    if func.variables[_v] != v_type:
                        errors.append(f'ERROR: Scanf expects \'%{specifier}\' - Found \'{_v} {func.variables[_v]}\'')
            ## checks return of main function
            # returnStatement = func.return_statement
            # checkReturn(returnStatement, func)



    if errors: printErrors()
    return 1 if errors else 0
