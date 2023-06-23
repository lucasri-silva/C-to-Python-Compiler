import re
import semantic_analyzer

num_errors = 0
errors = []
to_match = []

def create_new_c_file():
    file = open('Cprogram.c', 'r')
    new_file = open('Cprogram_modified.c', 'w')

    line_num = 0

    # Read the first line
    line = file.readline()

    while line:
        line_num += 1

        if line.strip():

            if line.strip()[:2] == '//':
                line = file.readline()
                continue

            if line.strip()[-1] == '{':
                new_file.write(str(line_num) + ': ' + line.strip()[:-1])
                new_file.write('\n' + str(line_num) + ': {\n')
                line = file.readline()
                continue

            if len(line.strip()) > 1 and line.strip()[-1] == '}':
                new_file.write(str(line_num) + ': ' + line.strip()[:-1])
                new_file.write('\n' + str(line_num) + ': }\n')
                line = file.readline()
                continue

            new_file.write(str(line_num) + ': ' + line.strip() + '\n')
        line = file.readline()

    file.close()
    new_file.close()


def check_regex(line):

    global num_errors
    global errors
    global to_match

    mainFuncionPattern = r"\w+\s*main\s*\(\s*void\s*\)\s*$"
    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    variablePattern = r"^((?:\w+|\"[^\"]*\"|\'[^\']*\')?\s*\w+)\s*(?:\=+\s*(\w+|\"[^\"]*\"|\'[^\']*\'))?(?:\s*[\+\-\/\*]\s*(\w+|\"[^\"]*\"|\'[^\']*\'))*\;$"
    scanfPattern = r'^(scanf)\("%([d|ld|f|lf|c|u|lu|x|o])+",&(\w+)\);$'
    printfPattern = r'^(printf)\("%([c|d|e|f|g|i|o|p|s|u|x])(\\n)?",(\w+)\);$'
    funcVariableAssignmentPattern = r'^(\w*\s*\w+)+\s*\=+\s*(\w+)\s*\(\s*(\w+\s*(?:,\s*\w+)*)?\s*\);$'
    returnFunctionPattern = r'^(\w+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*$'

    ## ignores the line number :
    line_wn = line[3:].strip()

    ## to match
    if to_match and re.match(to_match[0], line_wn):
        match = re.match(to_match[0], line_wn)
        semantic_analyzer.addReturn(match)
        to_match.remove(to_match[0])
        return

    ## include
    elif re.match(includePattern, line_wn):
        return

    ## functions that return something
    elif re.match(returnFunctionPattern, line_wn):
        
        if re.match(r'^(void+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s$', line_wn):
            match = re.match(r'^(void+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*$', line_wn)
            
            semantic_analyzer.addFunction(match)
            to_match.append('{')
            to_match.append('}')
            return

        match = re.match(returnFunctionPattern, line_wn)
        semantic_analyzer.addFunction(match)
        regex = r'^\s*return\s+.+\s*;$'
        to_match.append('{')
        to_match.append(regex)
        to_match.append('}')
        return

    ## main function
    elif re.match (mainFuncionPattern, line_wn):

        if re.match (r"^int\s+main\s*\(\s*void\s*\)\s*$", line_wn):
            match = re.match(r"^int\s+main\s*\(\s*void\s*\)\s*$", line_wn)
            semantic_analyzer.addMain(match)
            regex = r'^\s*return\s+.+\s*;$'
            to_match.append('{')
            to_match.append(regex)
            to_match.append('}')
            return

        match = re.match(mainFuncionPattern, line_wn)
        semantic_analyzer.addMain(match)
        to_match.append('{')
        to_match.append('}')
        return

    ## int a = 10
    elif re.match(variablePattern, line_wn):
        match = re.match(variablePattern, line_wn)
        semantic_analyzer.addVariable(match)
        return

    ## int a = somar(a, b)
    elif re.match(funcVariableAssignmentPattern, line_wn):
        match = re.match(funcVariableAssignmentPattern, line_wn)
        semantic_analyzer.addFunctionVariableAssignment(match)
        return

    ## scanf
    elif re.match(scanfPattern, line_wn):
        match = re.match(scanfPattern, line_wn)
        semantic_analyzer.addIO(match)
        return

    ## prinf
    elif re.match(printfPattern, line_wn):
        match = re.match(printfPattern, line_wn)
        semantic_analyzer.addIO(match)
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

                if line_wn[:-1] in to_match[0]:
                    print(f'matched {line} {to_match}')
                    to_match.remove(to_match[0])
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

    create_new_c_file()
    global num_errors
    global errors

    with open('Cprogram_modified.c', 'r') as file:

        line = file.readline()
        while line:
            check_regex(line.strip())
            line = file.readline()

    file.close()
    if errors: print_errors()

    return 1 if num_errors else 0
