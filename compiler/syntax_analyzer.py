import re

def syntax_analysis():
    with open('Cprogram.c', 'r') as file:

        includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
        returnFunctionPattern = r'^[int|float|double|char]+\s+\w+\s*\(\s*((?:[int|float|double|char]+\s+\w+\,\s*)*[int|float|double|char]+\s+\w+)\s*\)+\s*{\s*.*\s*return\s+((\w+(?:\s*[\+\-\/\*]\s*\w+)*)|(\(\w+(?:\s*[\+\-\/\*]\s*\w+)*)\));\s*.*\s*}$'
        mainFuncionPattern = r"int\s+main\s*\(\s*void\s*\)\s*{\s*((?:[^{}]*{[^{}]*})*[^{}]*?)\s*return\s+0;\s*}"
        intPattern = r"^int +\w +\= +\w+(?:\s*[\+\-\/\*]\s*\w+)*\;$"
        scanfPattern = r'^scanf\("%[d|ld|f|lf|c|u|lu|x|o]+",&\w+\);$'
        funcVariableAssignmentPattern = r'^[int|float|double|char]+\s+\w+\s+\=+\s+\w+\s*\(\s*((?:\w+\s*,\s*)*\w+)\s*\);$'
        printfPattern = r'^printf\("%[c|d|e|f|g|i|o|p|s|u|x]\\n?",\w+\);$'

        lineNumber = 1
        mainExpression = ''
        expression = ''
        # buildingExpression = False
        numCurlyBraces = 0
        insideMain = False
        firstTimeInsideMain = True
        errors = 0
        
        for line in file:
            if line.strip(): # ignore empty lines
                line = line.strip()
                line_splited = line.split()

                if insideMain or re.match(r'int\s+main\s*\(\s*(void)?\s*\)\s*{?', line):
                                    
                    if firstTimeInsideMain:
                        expression = ''
                        mainExpression += line
                        numCurlyBraces += 1
                        insideMain = True
                        firstTimeInsideMain = False
                        lineNumber += 1
                        continue

                    mainExpression += line
                    expression += line
                    
                    ## int a = 10
                    if re.match(r"^int +\w +(\=)? +\w+(?:\s*[\+\-\/\*]\s*\w+)*\;?$", expression):
                        if not re.match(intPattern, expression):
                            errors += 1
                            print(f'intPattern ERROR at line {lineNumber}: \n{expression}')

                    ## int a = somar(a, b)
                    elif re.match(r'^[int|float|double|char]+\s+\w+\s+(\=)?\s+\w+\s*\(\s*((?:\w+\s*,\s*)*\w+)\s*\);?$', expression):
                        if not re.match(funcVariableAssignmentPattern, expression):
                            errors += 1
                            print(f'funcVariableAssignmentPattern ERROR at line {lineNumber}: \n{expression}')

                    ## scanf
                    elif re.match(r'^scanf(.*)$', expression): 
                        if not re.match(scanfPattern, expression):
                            errors += 1
                            print(f'scanfPattern ERROR at line {lineNumber}: \n{expression}')

                    ## prinf
                    elif re.match(r'^printf(.*)$', expression):
                        if not re.match(printfPattern, expression):
                            errors += 1
                            print(f'printfPattern ERROR at line {lineNumber}: \n{expression}')

                    expression = ''

                if not insideMain:
                    
                    expression += line

                    if re.match(r'^#?include(.*)$', expression):
                        if not re.match(includePattern, expression):
                            errors += 1
                            print(f'includePattern ERROR at line {lineNumber}: \n{expression}')
                        expression = ''
                    
                    elif line_splited[-1][-1] == '{':
                        # buildingExpression = True
                        lineNumber += 1
                        numCurlyBraces += 1
                        continue

                    elif line_splited[-1][-1] == '}':
                        # buildingExpression = False
                        numCurlyBraces -= 1

                        if not re.match(returnFunctionPattern, expression):
                            errors += 1
                            print(f'returnFunctionPattern ERROR at line {lineNumber - 1}: \n{expression}')
                        expression = ''
            
            lineNumber += 1

        if not re.match(mainFuncionPattern, mainExpression):
            errors += 1
            print(f'mainFuncionPattern ERROR at line {lineNumber}')
        
    return 0 if errors == 0 else 1