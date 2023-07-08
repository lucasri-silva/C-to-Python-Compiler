import re
import semantic_analyzer

errors = []
to_match = []
conditionalBlock = False

def reset():
    global errors
    global to_match
    global conditionalBlock
    errors = []
    to_match = []
    conditionalBlock = []

def check_regex(line):

    global num_errors
    global errors
    global to_match
    global conditionalBlock

    mainFuncionPattern = r'int main\((.*?)\)'
    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    variableDeclarationPattern = r"(?:\b(?:int|float)\s+)(?:\w+\b(?:,\s*\w+\b)*)\s*;"
    variableDefinitionPattern = r"^(.*?)\s*=\s*(.*?)\s*;$"
    scanfPattern = r'^(scanf)\("%([f|i])+"\s*,\s*&(\w+)\);$'
    printfPattern = r'^printf\s*\("%([c|d|e|f|g|i|o|p|s|u|x])(\\n)?",(\w+)\);$'
    funcVariableAssignmentPattern = r'^(\w*\s*\w+)+\s*\=+\s*(\w+)\s*\(\s*(\w+\s*(?:,\s*\w+)*)?\s*\);$'
    returnFunctionPattern = r'^(\w+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*$'
    returnStatementPattern = r'^return\s+.+;$'
    ifStatementPattern = r"if\s*\((.*?)\s*(?:>|<)\s*(.*?)\)\s*"
    elseStatementPattern = r'else\s*'

    ## ignores the line number :
    line_wn = line[3:].strip()
    line_num = line.split(':')[0]

    ## to match
    if to_match and re.match(to_match[-1], line_wn):
        match = re.match(to_match[-1], line_wn)
        if 'return' in to_match[-1]:
            semantic_analyzer.addReturn(match)
        elif conditionalBlock and to_match[-1] == '}':
            semantic_analyzer.endOfConditional()
            conditionalBlock = False
        to_match.pop()
        return

    elif re.match(includePattern, line_wn):
        return

    elif re.match(returnFunctionPattern, line_wn):
        
        if re.match(r'^(void+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s$', line_wn):
            match = re.match(r'^(void+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*$', line_wn)
            
            semantic_analyzer.addFunction(match)
            to_match.append('}')
            to_match.append('{')
            return

        match = re.match(returnFunctionPattern, line_wn)
        semantic_analyzer.addFunction(match)
        to_match.append('}')
        regex = r'^\s*return\s+.+\s*;$'
        to_match.append(regex)
        to_match.append('{')
        return

    elif re.match(returnStatementPattern, line_wn):
        match = re.match(returnStatementPattern, line_wn)
        semantic_analyzer.addReturn(match)
        return

    elif re.match (mainFuncionPattern, line_wn):

        if re.match (r'int main\((.*?)\)', line_wn):
            match = re.match(r'int main\((.*?)\)', line_wn)
            semantic_analyzer.addMain(match)
            to_match.append('}')
            regex = r'^\s*return\s+.+\s*;$'
            to_match.append('{')
            to_match.append(regex)
            semantic_analyzer.addReturn(match)
            return

        match = re.match(mainFuncionPattern, line_wn)
        semantic_analyzer.addMain(match)
        to_match.append('}')
        regex = r'^\s*return\s+.+\s*;$'
        to_match.append('{')
        to_match.append(regex)
        return

    elif re.match(variableDeclarationPattern, line_wn):
        match = re.match(variableDeclarationPattern, line_wn)
        semantic_analyzer.addVariableDeclaration(match, line_num)
        return

    elif re.match(variableDefinitionPattern, line_wn):
        match = re.match(variableDefinitionPattern, line_wn)
        semantic_analyzer.addVariableDefinition(match, line_num)
        return

    elif re.match(funcVariableAssignmentPattern, line_wn):
        match = re.match(funcVariableAssignmentPattern, line_wn)
        semantic_analyzer.addFunctionVariableAssignment(match)
        return

    elif re.match(scanfPattern, line_wn):
        match = re.match(scanfPattern, line_wn)
        semantic_analyzer.addIO(match, line_num)
        return

    elif re.match(printfPattern, line_wn):
        match = re.match(printfPattern, line_wn)
        semantic_analyzer.addIO(match, line_wn)
        return

    elif re.match(ifStatementPattern, line_wn):
        match = re.match(ifStatementPattern, line_wn)
        to_match.append('}')
        to_match.append('{')
        semantic_analyzer.addIfStatement(match, line_num)
        return

    elif re.match(elseStatementPattern, line_wn):
        match = re.match(elseStatementPattern, line_wn)
        to_match.append('}')
        to_match.append('{')
        conditionalBlock = True
        semantic_analyzer.addElseStatement(match, line_num)
        return


    ## ERRORS
    else:
        # functions that return something
        if re.match(r'^(\w+)?\s+(\w+)?\s*\(?((\w+)?\s*\,*\s*)*\)?$', line_wn):
            errors.append(line)
            regex = r'^\s*return\s+.+\s*;$'
            to_match.append('{')
            to_match.append(regex)
            to_match.append('}')    
            return
        
        ## int a = 10
        elif re.match(r"^(\w+)?\s*\w+\s*(\=)?\s*\w+(?:\s*[\+\-\/\*]\s*\w+)*\;?$", line_wn):
            errors.append(line)
        
        ## int a = somar(a, b)
        elif re.match(r'^(\w*)?\s*\w+\s+(\=)?\s+(\w+)?\s*\(?\s*((?:(\w+)?\s*,\s*)*(\w+)?)\s*\)?;?$', line_wn):
            errors.append(line)

        ## printf
        elif re.match(r'^pr+(.*)$', line_wn):
            errors.append(line)

        ## scanf
        elif re.match(r'^sc+(.*)$', line_wn):
            errors.append(line)

        ## include
        elif re.match(r'^#?include(.*)$', line_wn):
            errors.append(line)

        ## to_match[0] nao deu match, logo tudo aquilo que esta no vetor to_match antes da expressao
        ## atual para dar match é dado como erro
        else:
            matched = False
            for exp in to_match:

                if line_wn[:-1] in to_match[-1]:
                    to_match.remove(to_match[-1])
                    matched = True
                    break

                else:
                    errors.append(line)
                    to_match.remove(exp)
            
    return


def print_errors():
    global errors
    global other_errors

    for error in errors:
        print(f'ERROR at line {error}')


def syntax_analysis():

    global num_errors
    global errors

    with open('modified.c', 'r') as file:

        line = file.readline()
        while line:
            check_regex(line.strip())
            line = file.readline()

    file.close()
    if errors: print_errors()

    return 1 if errors else 0
