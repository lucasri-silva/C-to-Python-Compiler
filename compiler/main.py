import lexical_analyzer
import syntax_analyzer
import semantic_analyzer

def main():
    
    # lexical_result = lexical_analyzer.lexical_analysis()

    # if lexical_result == 1:
    #     print('LEXICAL ERROR')
    #     return 0
    
    # syntax_result = syntax_analyzer.syntax_analysis()

    # if syntax_result == 1:
    #     print('SYNTAX ERROR')
    #     return 0
    
    semantic_result = semantic_analyzer.semantic_analysis()
        
    # if semantic_result == 1:
    #     print('SYNTAX ERROR')
    #     return 0

if __name__ == "__main__":
    main()    