import re

inside_main = False
main_expression = ''
errors = 0

def reposition_file_pointer(file, line):
    # Get the current position of the file pointer
    pos = file.tell()
    # Subtract the length of the current line (including the newline character) to move to the previous line
    prev_pos = pos - len(line)
    # Move the file pointer to the new position
    file.seek(prev_pos)

def create_new_c_file():
    file = open('Cprogram.c', 'r')
    new_file = open('Cprogram_inline.c', 'w')
    creating_new_file = True

    # Read the first line
    line = file.readline()

    block_expression = ''

    while line:


        if re.match(r'^(\w+)+\s+(\w+)?\s*\(?\s*((?:(\w*)?\s*(\w*)?,\s*)*(\w+)?\s+(\w*)?)\s*\)?\s*{?$', line.strip()):
            
            block_expression += line.rstrip()

            # Keep reading lines until we find the end of the function block
            while not check_regex(line.rstrip(), creating_new_file):
                line = file.readline()
                block_expression += line.rstrip()

            new_file.write(block_expression)
            block_expression = ''

        elif line.strip() == '}':
            reposition_file_pointer(new_file, line.strip())
            new_file.write('}\n')

        else:
            if line.strip():
                new_file.write(line.strip()+'\n')
        
        line = file.readline()
    
    file.close()
    new_file.close()


def read_next_line(file):
    line = file.readline() ## Read the next line
    return line

def check_regex(line, creating_new_file):

    global inside_main
    global main_expression
    global errors

    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    intPattern = r"^(\w+\s+\w+)\s*\=+\s*(\w+)(?:\s*[\+\-\/\*]\s*(\w+))*\;$"
    scanfPattern = r'^scanf\("%([d|ld|f|lf|c|u|lu|x|o])+",&(\w+)\);$'
    printfPattern = r'^printf\("%([c|d|e|f|g|i|o|p|s|u|x])\\n?",(\w+)\);$'
    funcVariableAssignmentPattern = r'^(\w*\s*\w+)+\s*\=+\s*\w+\s*\(\s*((?:\w+\s*,\s*)+\w+)\s*\);$'
    returnFunctionPattern = r'^(\w+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)\s*\)+\s*{\s*.*\s*(return\s+((\w+(?:\s*[\+\-\/\*]\s*\w+)*)|(\(\w+(?:\s*[\+\-\/\*]\s*\w+)*)\)));\s*.*\s*}$'

    ## include
    if re.match(r'^#?include(.*)$', line):
        if not re.match(includePattern, line) and not creating_new_file:
            print(f'ERROR: {line}')
            errors += 1
        return True
    
    ## functions that return something
    elif re.match(r'^(\w+)?\s+(\w+)?\s*\(?\s*((?:(\w+)?\s+\w*,\s*)*((\w+))?\s+(\w*))?\s*\)?\s*(\{)?(\s*.*\s*return\s+((\w+(?:\s*[\+\-\/\*]\s*\w+)*)|(\(\w+(?:\s*[\+\-\/\*]\s*\w+)*)\));?\s*.*\s*}?)?$', line):
        match = re.match(returnFunctionPattern, line)
        if not match and not creating_new_file:
            print(f'ERROR: {line}')
            errors += 1
        return True

    ## main function
    elif re.match (r"^int\s+main\s*\(\s*void\s*\)\s*{?$", line):
        inside_main = True
        main_expression += line
        return True
    
    ## int a = 10
    elif re.match(r"^\w+\s+\w+\s*(\=)?\s*\w+(?:\s*[\+\-\/\*]\s*\w+)*\;?$", line):
        match = re.match(intPattern, line)
        if not match and not creating_new_file:
            print(f'ERROR: {line}')
            errors += 1
        return True
        
    # int a = somar(a, b)
    elif re.match(r'^(\w*)?\s*\w+\s+(\=)?\s+(\w+)?\s*\(?\s*((?:\w+\s*,\s*)*\w+)\s*\)?;?$', line):
        match = re.match(funcVariableAssignmentPattern, line)
        if not match and not creating_new_file:
            print(f'ERROR: {line}')
            errors += 1
        return True
        
    ## scanf
    elif re.match(r'^s+(.*)$', line): 
        match = re.match(scanfPattern, line)
        if not match and not creating_new_file:
            print(f'ERROR: {line}')
            errors += 1
        return True

    ## prinf
    elif re.match(r'^p+(.*)$', line):
        match = re.match(printfPattern, line)
        if not match and not creating_new_file:
            print(f'ERROR: {line}')
            errors += 1
        return True
        
    elif not re.match(r'^return+s*.', line) and not creating_new_file:
        print(f'ERROR: {line}')

        
    return False



def syntax_analysis():

    create_new_c_file()
    global inside_main
    global main_expression
    global errors
    creating_new_file = False
    
    with open('Cprogram_inline.c', 'r') as file:

        mainFuncionPattern = r"int\s+main\s*\(\s*void\s*\)\s*{\s*((?:[^{}]*{[^{}]*})*[^{}]*?)\s*return\s+0;\s*}"
        
        # Read the first line
        line = file.readline()

        while line:

            ## outside the main function
            while not inside_main:

                check_regex(line.strip(), creating_new_file)
                line = read_next_line(file)
                
            ## inside the main function
            if inside_main:
                main_expression += line.strip()
                check_regex(line.strip(), creating_new_file)

            line = read_next_line(file)

    if not re.match(mainFuncionPattern, main_expression):
        print(f'ERROR main function')

    file.close()
        
    return 1 if errors else 0