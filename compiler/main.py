import lexical_analyzer
import syntax_analyzer

def main():
    
    lexical_result = lexical_analyzer.lexical_analysis()

    if lexical_result == 1:
        print('LEXICAL ERROR')
        return 0
    
    syntax_result = syntax_analyzer.syntax_analysis()

    if syntax_result == 1:
        print('SYNTAX ERROR')
        return 0
        

if __name__ == "__main__":
    main()    