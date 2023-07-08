import re
import os

to_match = []
conditionalBlock = False
indent = 1

def remove_comments(file_path):
    with open(file_path, 'r') as file:
        c_code = file.read()

    c_code = re.sub(r'/\*.*?\*/', '', c_code, flags=re.DOTALL)
    c_code = re.sub(r'//.*', '', c_code)

    return c_code


def check_regex(line, file):

    global to_match
    global conditionalBlock
    global indent

    mainFuncionPattern = r'int main\((.*?)\)'
    includePattern = r'^#include\s+((<[^>]+>)|("[^"]+"))$'
    variableDeclarationPattern = r"(?:\b(?:int|float)\s+)(?:\w+\b(?:,\s*\w+\b)*)\s*;"
    variableDefinitionPattern = r"^(.*?)\s*=\s*(.*?)\s*;?$"
    scanfPattern = r'^(scanf)\("%([f|i])+"\s*,\s*&(\w+)\);$'
    printfPattern = r'^\s*printf\s*\("%([cdefgiosux])",\s*(\w+)\);\s*$'
    returnFunctionPattern = r'^(\w+\s+\w+)\s*\(\s*((?:\w+\s+\w+\,\s*)*\w+\s+\w+)?\s*\)+\s*{$'
    ifStatementPattern = r"if\s*\((.*?)\s*(?:>|<)\s*(.*?)\)\s*"
    elseStatementPattern = r'else\s*'

    ## to match
    if to_match and re.match(to_match[-1], line):
        match = re.match(to_match[-1], line)
        if 'return' in to_match[-1]:
            conditionalBlock = False
            indent -= 1
        elif conditionalBlock and to_match[-1] == '}':
            conditionalBlock = False
            indent -= 1
            file.write('\n')
        to_match.pop()
        return

    if re.match(includePattern, line):
        return

    elif re.match(returnFunctionPattern, line):
        match = re.match(returnFunctionPattern, line)
        variables = re.findall(r'\b\w+\b', match[0])
        code = ', '.join(variables[1:])
        code = line.replace('float', '')
        code = code.replace('int', '')
        code = code.replace('void', '')
        code = code.replace('{', ':')
        file.write('def ' + code.strip())
        file.write('\n')
        to_match.append('}')
        regex = r'^\s*return\s+.+\s*;$'
        to_match.append(regex)
        to_match.append('{')
        conditionalBlock = True
        indent = 1
        to_match.append('}')
        return

    if re.match (mainFuncionPattern, line):
        file.write('def main():')
        indent = 1
        file.write('\n')

    elif re.match(r'^\s*return\s+.+\s*;$', line):
        match = re.match(r'^\s*return\s+.+\s*;$', line)
        variables = re.findall(r'\b\w+\b', match[0])
        file.write(indent * '\t' + line)
        file.write('\n')
        return

    elif re.match(variableDeclarationPattern, line):
        match = re.match(variableDeclarationPattern, line)
        variables = re.findall(r'\b\w+\b', match[0])
        code = ', '.join(variables[1:])
        code = code + ' = ' + len(variables[1:]) * 'None, '
        file.write(indent * '\t' + code[:-2])
        file.write('\n')
        return

    elif re.match(variableDefinitionPattern, line):
        match = re.match(variableDefinitionPattern, line)
        code = re.sub(r'\bfloat\b', '', line, flags=re.MULTILINE)
        code = re.sub(r'\bint\b', '', code, flags=re.MULTILINE)
        code = code.replace('()', '')
        file.write(indent * '\t' + code.strip())
        file.write('\n')
        return

    elif re.match(scanfPattern, line):
        match = re.match(scanfPattern, line)
        variables = re.findall(r'\b\w+\b', match[0])
        v_type = ''
        if variables[1] == 'i':
            v_type = 'int'
        elif variables[1] == 'f':
            v_type = 'float'
        code = (f'{variables[-1]} = {v_type}(input())') 
        file.write(indent * '\t' + code)
        file.write('\n')
        return

    elif re.match(printfPattern, line):
        match = re.match(printfPattern, line)
        variables = re.findall(r'\b\w+\b', match[0])
        code = f'print({variables[-1]})'
        file.write(indent * '\t' + code)
        file.write('\n')
        return

    elif re.match(ifStatementPattern, line):
        to_match.append('}')
        code = line.replace('(', '')
        code = code.replace(')', '')
        code = code.replace('{', ':')
        file.write(indent * '\t' + code)
        file.write('\n')
        conditionalBlock = True
        indent += 1
        return
    
    elif re.match(elseStatementPattern, line):
        to_match.append('}')
        code = line.replace('{', ':')
        file.write(indent * '\t' + code)
        file.write('\n')
        indent += 1
        conditionalBlock = True
        return

    return


def translator():
    files = os.listdir('../test/')
    for file_name in files:
        file_path = os.path.join('../test/', file_name)

        clean_code = remove_comments(file_path)
        file_name = file_name.split('.')[0]
        path = './translated_code/' + file_name + '.py'
        new_file = open(path, 'w')
        lines = clean_code.splitlines()

        for line in lines:
            check_regex(line.strip(), new_file)

        new_file.write('\nif __name__ == "__main__":\n\tmain()')
        new_file.close()

    return 0
