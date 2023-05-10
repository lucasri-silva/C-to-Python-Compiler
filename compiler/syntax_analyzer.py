import re

errors = 0
to_match = []

def reposition_file_pointer(file, line):
    # Get the current position of the file pointer
    pos = file.tell()
    # Subtract the length of the current line (including the newline character) to move to the previous line
    prev_pos = pos - len(line)
    # Move the file pointer to the new position
    file.seek(prev_pos)

def create_new_c_file():
    file = open('Cprogram.c', 'r')
    new_file = open('Cprogram_modified.c', 'w')

    # Read the first line
    line = file.readline()

    while line:

        if line.strip():
            line = file.readline()
            continue

        if line.strip() == '}':
            reposition_file_pointer(new_file, line.strip())
            new_file.write('}\n')
            line = file.readline()
            continue

        new_file.write(line.strip()+'\n')
        line = file.readline()
    
    file.close()
    new_file.close()


def read_next_line(file):
    line = file.readline() ## Read the next line
    return line

def check_regex(line):

    global errors
    global to_match

    mainFuncionPattern = r"\w+\s*main\s*\(\s*void\s*\)\s*{?"
    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    intPattern = r"^(\w+\s+\w+)\s*\=+\s*(\w+)(?:\s*[\+\-\/\*]\s*(\w+))*\;$"
    scanfPattern = r'^scanf\("%([d|ld|f|lf|c|u|lu|x|o])+",&(\w+)\);$'
    printfPattern = r'^printf\("%([c|d|e|f|g|i|o|p|s|u|x])\\n?",(\w+)\);$'
    funcVariableAssignmentPattern = r'^(\w*\s*\w+)+\s*\=+\s*\w+\s*\(\s*(\w+\s*(?:,\s*\w+)*)?\s*\);$'
    returnFunctionPattern = r'^(\w+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*{?$'

    print(line)

    ## to match
    if to_match and re.match(to_match[0], line):
        to_match.pop()
        print(f'removed ----- {line}')
        return True

    ## include
    if re.match(r'^#?include(.*)$', line):
        if not re.match(includePattern, line):
            print(f'ERROR includePattern: {line}')
            errors += 1
        
        print(f'matched {line}')
        return True
    
    ## functions that return something
    elif re.match(r'^(\w+)?\s+(\w+)?\s*\(?\s*((?:(\w+)?\s+\w*,\s*)*((\w+))?\s+(\w*))?\s*\)?\s*\{?$', line):
        match = re.match(returnFunctionPattern, line)
        if not match:
            print(f'ERROR returnFunctionPattern: {line}')
            errors += 1
        print(f'matched {line}')
        regex = r'^return+\s+\w+\;$'
        to_match.insert(0, regex)
        # for word in to_match: print(word)
        print(to_match)
        return True

    ## main function
    elif re.match (r"^int\s+main\s*\(\s*void\s*\)\s*{?$", line):
        print(f'matched {line}')
        return True
    
    ## int a = 10
    elif re.match(r"^\w+\s+\w+\s*(\=)?\s*\w+(?:\s*[\+\-\/\*]\s*\w+)*\;?$", line):
        match = re.match(intPattern, line)
        if not match:
            print(f'ERROR intPattern: {line}')
            errors += 1
        print(f'matched {line}')
        return True
        
    # int a = somar(a, b)   
    elif re.match(r'^(\w*\s*\w+)?\s*\=+\s*(\w+)?\s*\(\s*(\w+\s*(?:,\s*\w+)*)?\s*\);$', line):
        match = re.match(funcVariableAssignmentPattern, line)
        if not match:
            print(f'ERROR funcVariableAssignmentPattern: {line}')
            errors += 1
        print(f'matched {line}')
        return True
        
    ## scanf
    elif re.match(r'^s+(.*)$', line): 
        match = re.match(scanfPattern, line)
        if not match:
            print(f'ERROR scanfPattern: {line}')
            errors += 1
        print(f'matched {line}')
        return True

    ## prinf
    elif re.match(r'^p+(.*)$', line):
        match = re.match(printfPattern, line)
        if not match:
            print(f'ERROR printfPattern: {line}')
            errors += 1
        print(f'matched {line}')
        return True
        
    else:
        print(f'ERROR ultimo: {line}')

        
    return False



def syntax_analysis():

    create_new_c_file()
    global errors
    
    with open('Cprogram_modified.c', 'r') as file:

        # Read the first line
        line = file.readline()

        while line:

            print(line)
            check_regex(line.strip())
            line = read_next_line(file)

    file.close()
        
    return 1 if errors else 0