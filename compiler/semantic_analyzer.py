import re

linhas_tratadas = []

def semantic_analysis():

    print("Analisador SemÂntico!")

    print("\n\nLeitura e tratamento do código em C")
    with open('Cprogram.c', 'r') as arquivo:
        for linha in arquivo:
            linha_sem_espacos = linha.strip()
            linhas_tratadas.append(linha_sem_espacos)   
            print(linha_sem_espacos)

    print("\n\nLinhas armazenadas em uma lista")
    print(linhas_tratadas)

    print("\n\nRegex do padrão de função: (\w+)\s+(\w+)\s*\([^)]*\)\s*{")
    padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
    print("\n\nRegex do padrão de include: #include\s+(<\w+\.h>|'[\w\.]+' ")
    padrao_include = r'#include\s+(<\w+\.h>|"[\w\.]+")'

    print("\n\nFim\n\n")