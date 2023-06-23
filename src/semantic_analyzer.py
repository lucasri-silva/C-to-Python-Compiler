import re

errors = []
funcName = ''
function_list = []

class FunctionInfo:
    def __init__(self, name, return_type, parameters):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.variables = []
        self.body = [] 
        self.return_statement = []

    def display_info(self):
        print("Name: ", self.name)
        print("Return Type: ", self.return_type)
        print("Parameters:", self.parameters)
        print("Variables: ", self.variables)
        print("Body:", self.body)
        print("Return Statement:", self.return_statement)

def addBodyFunctionInfo(funcName, variables):
    for func in function_list:
        if func.name == funcName:
            func.body.append(variables)
            break

def addReturnFunctionInfo(funcName, variables):
    for func in function_list:
        if func.name == funcName:
            func.return_statement.extend(variables)
            break

def addVariableFunctionInfo(funcName, variables):
    for func in function_list:
        if func.name == funcName:
            func.variables.append(variables)
            break;
        
def addFunction(match):
    global funcName
    global function_list
    variables = re.findall(r'\b\w+\b', match[0])
    funcName = variables[1]
    f = FunctionInfo(variables[1], variables[0], variables[2:])
    function_list.append(f)

def addVariable(match):
    global funcName
    variables = re.findall(r'\b\w+\b', match[0])
    if variables[0] in ['int', 'float', 'string', 'char']:
        addVariableFunctionInfo(funcName, variables[:2])
    variables[0] = 'v ' + variables[0]
    addBodyFunctionInfo(funcName, variables)

def addReturn(match):
    global funcName
    variables = re.findall(r'\b\w+\b', match[0])
    addReturnFunctionInfo(funcName, variables[1:])

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

def addIO(match):
    global funcName
    global function_list
    variables = re.findall(r'\b\w+\b', match[0])
    if len(variables) > 3 and 'n' in variables:
        variables.remove('n')
    variables[0] = 'io ' + variables[0]
    addBodyFunctionInfo(funcName, variables)

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

    elif aux_type == 'io' and variable in ['d','f','s','c']:
        if variable == 'd':
            v_type = 'int'
        elif variable == 'f':
            v_type = 'float'
        elif variable == 's':
            v_type = 'string'
        elif variable == 'c':
            v_type = 'char'

    return v_type
    
def printErrors():
    for error in errors:
        print(error)

def semantic_analysis():
    # printFuncList()

    for func in function_list:
        ## verify all functions but main function
        if func.name != 'main':

            for r in func.return_statement:
                found = False

                ## verify if function return matches
                for index, p in enumerate(func.parameters):
                    if r == p:
                        found = True
                        if func.parameters[index-1] != func.return_type:
                            errors.append(f'ERROR: In function \'{func.name}\' return does not match. Expected \'{func.return_type}\' - Found \'{func.parameters[index-1]}\'')
                            break

                if not found:
                    for index, b in enumerate(func.body):
                        if r == b:
                            found = True
                            if func.body[index-1] != func.return_type:
                                errors.append(f'ERROR: In function \'{func.name}\' return does not match. Expected \'{func.return_type}\' - Founded \'{func.parameters[index-1]}\'')
                                break

                if not found:
                    errors.append(f'ERROR: In \'{func.name}\', \'{r}\' is not defined.')
        ## main function
        else:
            for index, b in enumerate(func.body):
                aux_type = b[0].split()[0]

                if aux_type == 'v':
                    v_type = ''
                    found = False
                    if len(b) > 2:
                        v_value = b[2]
                    else:
                        v_value = b[1]

                    for v in func.variables:
                        ## verify if variable is in variables
                        if v[1] == b[1]:
                            found = True
                            v_type = v[0]
                            break
                    ## verify if variable value matches variable type
                    if found:
                        ## verify if function is assigned to variable
                        if v_value.split()[0] == 'fc':
                            func_parameters = b[3:]
                            for func_called in function_list:
                                if func_called.name == v_value.split()[1]:
                                    ## verify if variable type matches function return
                                    if func_called .return_type != v_type:
                                        errors.append(f'ERROR: Function \'{func_called .name}\' return type does not match \'{v_type} {v[1]}\'. Expected \'{v_type}\' - Found \'{func_called.return_type}\'')

                                    ## verify if number of parameters matches original function 
                                    if int(len(func_called .parameters)/2) != len(func_parameters): 
                                        errors.append(f'ERROR: Function \'{func_called .name}\' expects {int(len(func_called .parameters)/2)} parameters - Found {len(func_parameters)}')
                                        break
                                    ## verify if type of function call parameters matches original function
                                    for param in func_parameters:
                                        found = False
                                        for v in func.variables:
                                            if param == v[1]:
                                                v_type = v[0]
                                                found = True
                                                break

                                        if not found:
                                            errors.append(f'ERROR: In function \'{func_called.name}\' call, \'{param}\' is not defined')

                                        else:
                                            for index, p in enumerate(func_called.parameters):
                                                if p == param:
                                                    if func_called.parameters[index-1] != v_type:
                                                        errors.append(f'ERROR: Function \'{func_called.name}\' expects parameters {func_called.parameters} - Found \'{v_type} {p}\'')
                                                    break


                        else: 
                            type_found = checkVariableType(v_value, aux_type)
                            if type_found != v_type:
                                errors.append(f'ERROR: In function \'{func.name}\', there is a type mismatch. Expected \'{v_type} {v[1]}\' - Found \'{type_found}\'')
                    ## variable is not defined
                    else:
                        if v_type not in ['int', 'float', 'double']:
                            errors.append(f'ERROR: {v_type} is not defined.')
                        else:
                            errors.append(f'ERROR: {b[1]} is not defined.')
                    
                ## varify if specifier of scanf and printf matches 
                elif aux_type == 'io':

                    expected_type = '' 
                    specifier = b[1]
                    v_type = checkVariableType(specifier, aux_type)
                    for v in func.variables:
                        if v[1] == b[2]:
                            expected_type = v[0]
                            break

                    if v_type != expected_type:
                        if b[0].split()[1] == 'scanf':
                            errors.append(f'ERROR: Scanf expects \'%{specifier}\' - Found \'{expected_type}\'')
                        else:
                            errors.append(f'ERROR: Printf expects \'%{specifier}\' - Found \'{expected_type}\'')



    if errors: printErrors()
    return 1 if errors else 0
