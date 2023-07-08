import re

def add_line_to_modified_file(line, new_file, line_num):

    if len(line.strip()) > 1 and line.strip()[-1] == '{':
        new_file.write(str(line_num) + ': ' + line.strip()[:-1])
        new_file.write('\n' + str(line_num) + ': {\n')
        return

    if len(line.strip()) > 1 and line.strip()[-1] == '}':
        new_file.write(str(line_num) + ': ' + line.strip()[:-1])
        new_file.write('\n' + str(line_num) + ': }\n')
        return

    new_file.write(str(line_num) + ': ' + line.strip() + '\n')

def lexical_analysis(file):
    file = open(file, 'r')
    new_file = open('modified.c', 'w')
    invalid_characters = set()
    axiomas = []
    pattern = r'\s|(?<=[();,])|(?=[();,])'

    line = file.readline()
    line_num = 1

    while line:

        if line.strip():
            line_splitted = re.split(pattern, line.strip())
            for axioma in line_splitted:
                if '//' in axioma: 
                    match = re.search('//', line.strip())
                    line = line.strip()[:match.start()]
                    break
                elif axioma != '':
                    axiomas.append(axioma)
            
            add_line_to_modified_file(line, new_file, line_num) 
        line = file.readline()
        line_num += 1

    ## axiomas
    # print(axiomas)
    
    valid_characters = r"[A-Za-z0-9_+\-*/%<>=!&|\"'`‘“@^\$#~?:,;.(){}[\]\t\n\r\\]"

    for axioma in axiomas:
        for ch in axioma:
            if not re.findall(valid_characters, ch):
                invalid_characters.add(ch)
                print(f"Invalid character found: {ch}")

    file.close()
    new_file.close()

    return 1 if invalid_characters else 0
