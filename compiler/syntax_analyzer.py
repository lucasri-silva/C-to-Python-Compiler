import re

inside_main = False
main_expression = ''
errors = 0

def reposition_file_pointer(file, line):
    # Get the current position of the file pointer
    pos = file.tell()
    # Subtract the length of the current line (including the newline character) to move to the previous line
    prev_pos = pos - len(line) + 1
    # Move the file pointer to the new position
    file.seek(prev_pos)


def create_new_c_file():
    file = open('Cprogram.c', 'r')
    new_file = open('Cprogram_inline.c', 'w')

    # Read the first line
    line = file.readline()

    block_expression = ''

    while line:

        if re.match(r'^[int]+\s+\w+\s*\(\s*((?:[int]+\s+\w*,\s*)*[int]+\s+\w*)\s*\)+\s*{?$', line.strip()):
            
            block_expression += line.rstrip()

            while re.match(r'^[int]+\s+\w+\s*\(\s*((?:[int]+\s+\w*,\s*)*[int]+\s+\w*)\s*\)+\s*(\{?)\s*.*\s*return\s+((\w+(?:\s*[\+\-\/\*]\s*\w+)*)|(\(\w+(?:\s*[\+\-\/\*]\s*\w+)*)\));\s*.*\s*}?$', block_expression):
                
                line = file.readline()
                block_expression += line.rstrip()
            
            new_file.write(block_expression)
            block_expression = ''

        elif line.strip() == '}':
            reposition_file_pointer(new_file, line)
            new_file.write(line.strip()+'\n')

        else:
            if line.strip():
                new_file.write(line.strip()+'\n')
        
        line = file.readline()
    
    file.close()
    new_file.close()


def read_next_line(file):
    line = file.readline() ## Read the next line
    return line


def check_regex(line):

    global inside_main
    global main_expression
    global errors

    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    intPattern = r"^int +\w +\= +\w+(?:\s*[\+\-\/\*]\s*\w+)*\;$"
    scanfPattern = r'^scanf\("%[d|ld|f|lf|c|u|lu|x|o]+",&\w+\);$'
    printfPattern = r'^printf\("%[c|d|e|f|g|i|o|p|s|u|x]\\n?",\w+\);$'
    funcVariableAssignmentPattern = r'^[int|float|double|char]+\s+\w+\s+\=+\s+\w+\s*\(\s*((?:\w+\s*,\s*)*\w+)\s*\);$'
    returnFunctionPattern = r'^[int]+\s+\w+\s*\(\s*((?:[int]+\s+\w+\,\s*)*[int]+\s+\w+)\s*\)+\s*{\s*.*\s*return\s+((\w+(?:\s*[\+\-\/\*]\s*\w+)*)|(\(\w+(?:\s*[\+\-\/\*]\s*\w+)*)\));\s*.*\s*}$'
    
    ## include
    if re.match(r'^#?include(.*)$', line):
        if not re.match(includePattern, line):
            print(f'includePattern ERROR: {line}')
            errors += 1
    
    ## functions that return something
    elif re.match(r'^[int]+\s+\w+\s*\(\s*((?:[int]+\s+\w*,\s*)*[int]+\s+\w*)\s*\)+\s*(\{)?(\s*.*\s*return\s+((\w+(?:\s*[\+\-\/\*]\s*\w+)*)|(\(\w+(?:\s*[\+\-\/\*]\s*\w+)*)\));\s*.*\s*}?)?$', line):
        
        if not re.match(returnFunctionPattern, line):
            print(f'returnFunctionPattern ERROR: {line}')
            errors += 1

    ## main function
    elif re.match (r"^int\s+main\s*\(\s*void\s*\)\s*{?$", line):
        inside_main = True
        main_expression += line
        return True
    
    ## int a = 10
    elif re.match(r"^int +\w +(\=)? +\w+(?:\s*[\+\-\/\*]\s*\w+)*\;?$", line):
        if not re.match(intPattern, line):
            print(f'intPattern ERROR: {line}')
            errors += 1
        
    # int a = somar(a, b)
    elif re.match(r'^[int|float|double|char]+\s+\w+\s+(\=)?\s+\w+\s*\(\s*((?:\w+\s*,\s*)*\w+)\s*\)?;?$', line):
        if not re.match(funcVariableAssignmentPattern, line):
            print(f'funcVariableAssignmentPattern ERROR: {line}')
            errors += 1
        
    ## scanf
    elif re.match(r'^scanf(.*)$', line): 
        if not re.match(scanfPattern, line):
            print(f'scanfPattern ERROR: {line}')
            errors += 1

    ## prinf
    elif re.match(r'^printf(.*)$', line):
        if not re.match(printfPattern, line):
            print(f'printfPattern ERROR: {line}')
            errors += 1
        
    return False



def syntax_analysis():

    create_new_c_file()
    global inside_main
    global main_expression
    global errors
    
    with open('Cprogram_inline.c', 'r') as file:

      
        mainFuncionPattern = r"int\s+main\s*\(\s*void\s*\)\s*{\s*((?:[^{}]*{[^{}]*})*[^{}]*?)\s*return\s+0;\s*}"
        
        # Read the first line
        line = file.readline()

        while line:

            ## outside the main function
            while not inside_main:

                check_regex(line.strip())
                line = read_next_line(file)
                
            ## inside the main function
            if inside_main:
                main_expression += line.strip()
                check_regex(line.strip())

            line = read_next_line(file)

    if not re.match(mainFuncionPattern, main_expression):
        print(f'mainFuncionPattern ERROR')

    file.close()
        
    return 1 if errors else 0