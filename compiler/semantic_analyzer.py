import re

linhas_tratadas = []

codigo_fonte = '''
#include <stdio.h>>

int somar (int a, int b) {
  int x = 10
  return (a+b)
}

int subtrair (int a,) {
  return (a-b);
}

int multiplicar (int a, int b {
  return (a*b);
}

void dividir (int b) {
  a = b + 10;
}

int main(void) {
  int a = 10;
  b = 2;
  scaf("%d",&a);
  scanf("%d",&b);
  int c = somar(a,b);
  int d = subtrair(a,b);
  int e = multiplicar(a,b);
  int f = dividir(a,);
  printf("%d\n",a);
  printf("%\n",d);
  printf("%d\n",e);
  printf("%d\n",f);
  return 0;
  }
'''

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
    # padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
    print("\n\nRegex do padrão de include: #include\s+(<\w+\.h>|'[\w\.]+' ")
    # padrao_include = r'#include\s+(<\w+\.h>|"[\w\.]+")'

    print("\n\nFunções e seus retornos:")
    padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
    funcoes = re.findall(padrao_funcao, codigo_fonte)
    funcoes_dict = {nome: tipo for tipo, nome in funcoes}
    print(funcoes_dict)

    print("\n\nVariáveis e seus retornos:")
    padrao_funcao_var = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{([^}]*)}'
    funcoes = re.findall(padrao_funcao_var, codigo_fonte)
    variaveis_retornos = {}
    for tipo, nome, corpo in funcoes:
        padrao_variavel = r'\b{}\b'.format(nome)
        variaveis = re.findall(padrao_variavel, corpo)
        variaveis_retornos[nome] = (tipo, variaveis)

    print(variaveis_retornos)

    print("\n\nEncontra erros semânticos no código: ")
    # padrao_funcao_var2 = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{([^}]*)}'
    funcoes = re.findall(padrao_funcao_var, codigo_fonte)
    for tipo, nome, corpo in funcoes:
        padrao_variavel = r'(\w+)\s+(\w+)\s*;'
        variaveis = re.findall(padrao_variavel, corpo)
        for var_tipo, var_nome in variaveis:
            if var_tipo != tipo:
                print(f"A variável '{var_nome}' dentro da função '{nome}' retorna um valor de tipo diferente ({var_tipo} em vez de {tipo}).")

    print("\n\nEncontra erros de escopo no código: ")
    padrao_chave_abertura = r'{'
    padrao_chave_fechamento = r'}'
    escopos = []
    posicoes_chaves = []
    for match in re.finditer(padrao_chave_abertura, codigo_fonte):
        posicoes_chaves.append((match.start(), 'abertura'))
    for match in re.finditer(padrao_chave_fechamento, codigo_fonte):
        posicoes_chaves.append((match.start(), 'fechamento'))
    posicoes_chaves.sort()
    for posicao, tipo in posicoes_chaves:
        if tipo == 'abertura':
            escopos.append(posicao)
        else:
            if len(escopos) > 0:
                escopos.pop()
            else:
                print("Erro de escopo: chave de fechamento sem abertura correspondente.")

    if len(escopos) > 0:
        print("Erro de escopo: chave de abertura sem fechamento correspondente.")

    print("\n\nFim\n\n")