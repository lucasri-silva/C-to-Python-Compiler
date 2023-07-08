import lexical_analyzer
import syntax_analyzer
import semantic_analyzer

import sys
import os

def clear_terminal():
    if os.name == 'posix':  # For UNIX/Linux/Mac OS
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')

def main():
    files = ['código1.txt','código2.txt','código3.txt','código4.txt','código5.txt','código6.txt','código7.txt','código8.txt','código9.txt','código10.txt']

    for file in files:
        print(f'============ ARQUIVO {file}') 
        print("\n\nAnalisador Léxico")
        lexical_result = lexical_analyzer.lexical_analysis('../test/'+file)

        if lexical_result == 1:
            print('LEXICAL ERROR')
        else:
            print("No lexical errors")
        
            print("\n\nAnalisador Sintático")
            syntax_result = syntax_analyzer.syntax_analysis()

            if syntax_result == 1:
                print('SYNTAX ERROR')
            else:
                print("No syntax errors")

                print("\n\nAnalisador Semántico")
                semantic_result = semantic_analyzer.semantic_analysis()

                if semantic_result == 1:
                    print('SEMANTIC ERROR')
                else:
                    print("No semantic errors")

        syntax_analyzer.reset()
        semantic_analyzer.reset()
        input('Press any key to continue')
        clear_terminal()


if __name__ == "__main__":
    main()    
