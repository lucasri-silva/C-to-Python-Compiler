import re

errors = 0
to_match = []
# num_lines = 0

def create_new_c_file():
    file = open('Cprogram.c', 'r')
    new_file = open('Cprogram_modified.c', 'w')
    
    # num_lines_file = 0
    # num_lines_newfile = 0

    # Read the first line
    line = file.readline()

    while line:
        # num_lines_file += 1

        if line.strip():

            if line.strip()[-1] == '{':
                new_file.write(line.strip()[:-1])
                new_file.write('\n{\n')
                line = file.readline()
                # num_lines_newfile += 2
                continue

            if len(line.strip()) > 1 and line.strip()[-1] == '}':
                new_file.write(line.strip()[:-1])
                new_file.write('\n}\n')
                # num_lines_newfile += 2                
                line = file.readline()
                continue

            new_file.write(line.strip()+'\n')
        # num_lines_newfile += 1
        line = file.readline()

    file.close()
    new_file.close()
    # print(num_lines_file)
    # print(num_lines_newfile)


def check_regex(line):

    global errors
    global to_match

    voidMainFuncionPattern = r"\w+\s*main\s*\(\s*void\s*\)\s*$"
    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    intPattern = r"^(\w+\s+\w+)\s*\=+\s*(\w+)(?:\s*[\+\-\/\*]\s*(\w+))*\;$"
    scanfPattern = r'^scanf\("%([d|ld|f|lf|c|u|lu|x|o])+",&(\w+)\);$'
    printfPattern = r'^printf\("%([c|d|e|f|g|i|o|p|s|u|x])(\\n)?",(\w+)\);$'
    funcVariableAssignmentPattern = r'^(\w*\s*\w+)+\s*\=+\s*\w+\s*\(\s*(\w+\s*(?:,\s*\w+)*)?\s*\);$'
    returnFunctionPattern = r'^(\w+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*$'

    ## to match
    if to_match and re.match(to_match[0], line):
        to_match.remove(to_match[0])
        return

    ## include
    if re.match(includePattern, line):
        return
    
    ## functions that return something
    elif re.match(returnFunctionPattern, line):
        regex = r'^\s*return\s+.+\s*;$'
        to_match.append('{')
        to_match.append(regex)
        to_match.append('}')
        return

    ## main function
    elif re.match (voidMainFuncionPattern, line):
        if re.match (r"^int\s+main\s*\(\s*void\s*\)\s*$", line):
            regex = r'^\s*return\s+.+\s*;$'
            to_match.append('{')
            to_match.append(regex)
            to_match.append('}')
            return
        to_match.append('{')
        to_match.append('}')
        return
    
    ## int a = 10
    elif re.match(intPattern, line):
        return
        
    # int a = somar(a, b)   
    elif re.match(funcVariableAssignmentPattern, line):
        return
        
    ## scanf
    elif re.match(scanfPattern, line):
        return

    ## prinf
    elif re.match(printfPattern, line):
        return
        
    else:
        print(f'ERROR: {line}')
        return

        

def syntax_analysis():

    create_new_c_file()
    global errors
    
    with open('Cprogram_modified.c', 'r') as file:

        # Read the first line
        line = file.readline()

        while line:

            check_regex(line.strip())
            line = file.readline()

    file.close()
    print(to_match)
        
    return 1 if errors else 0