import re

linhas_tratadas = []
errors = []
tokens = ['return','scanf']

codigo_fonte = '''
#include <stdio.h>>

int somar (int a, float b) {
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
  float d = subtrair(a,b);
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
    print("Encontrando erros semânticos no código:")

    # Verificar erros de declaração de função
    padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
    funcoes = re.findall(padrao_funcao, codigo_fonte)

    # Armazenar as funções e seus tipos em uma lista
    lista_funcoes = []
    for tipo, nome in funcoes:
        lista_funcoes.append((tipo, nome))

        if tipo not in ['void', 'int', 'float', 'double', 'char']:
            print(f"Erro semântico: Tipo de retorno inválido na função '{nome}'.")

    # print(lista_funcoes)

    # Verificar erros de declaração de variáveis
    padrao_variavel = r'(\w+)\s+(\w+)\s*[,;=)]'
    variaveis = re.findall(padrao_variavel, codigo_fonte)

    # Armazenar as variáveis em uma lista
    lista_variaveis = []
    for tipo, nome in variaveis:
        lista_variaveis.append((tipo, nome))

        if tipo not in ['void', 'int', 'float', 'double', 'char'] and nome != '0':
            print(f"Erro semântico: Tipo de variável inválido na declaração de '{nome}'.")

    # print(lista_variaveis)
    conjunto_variaveis = set(lista_variaveis)
    # print(conjunto_variaveis)

    # Criar um dicionário para associar as variáveis a cada função
    funcoes_variaveis = {}

    for tipo, nome in funcoes:
        variaveis_funcao = []
        padrao_variavel_funcao = fr'{tipo}\s+(\w+)'
        variaveis = re.findall(padrao_variavel_funcao, codigo_fonte)

        for nome_variavel in variaveis:
            if nome_variavel in codigo_fonte:
                variaveis_funcao.append(nome_variavel)

        funcoes_variaveis[nome] = variaveis_funcao

        if tipo not in ['void', 'int', 'float', 'double', 'char']:
            print(f"Erro semântico: Tipo de retorno inválido na função '{nome}'.")

    # # Imprimir as variáveis associadas a cada função
    # for nome_funcao, variaveis_funcao in funcoes_variaveis.items():
    #     if variaveis_funcao:
    #         print(f"Função '{nome_funcao}':")
    #         for variavel in variaveis_funcao:
    #             print(f"- Variável '{variavel}'")

    # Verificar erros de declaração de função
    padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
    funcoes = re.findall(padrao_funcao, codigo_fonte)
    for tipo, nome in funcoes:
        if tipo not in ['void', 'int', 'float', 'double', 'char']:
            print(f"Erro semântico: Tipo de retorno inválido na função '{nome}'.")

    # Verificar erros de declaração de variáveis
    padrao_variavel = r'(\w+)\s+(\w+)\s*[,;=)]'
    variaveis = re.findall(padrao_variavel, codigo_fonte)
    for tipo, nome in variaveis:
        if tipo not in ['void', 'int', 'float', 'double', 'char'] and nome != '0':
            print(f"Erro semântico: Tipo de variável inválido na declaração de '{nome}'.")

    # Verificar erros de variáveis nos parâmetros de função
    padrao_parametro = r'\(\s*(\w+)\s+(\w+)\s*\)'
    parametros_funcao = re.findall(padrao_parametro, codigo_fonte)
    for tipo, nome in parametros_funcao:
        if tipo not in ['void', 'int', 'float', 'double', 'char'] and nome != '0':
            print(f"Erro semântico: Tipo de variável inválido no parâmetro da função '{nome}'.")

    # Lista para armazenar os erros encontrados
    erros = []

    for tipo_funcao, nome_funcao in lista_funcoes:
        for tipo, nome in funcoes:
            padrao_variavel_funcao = fr'{tipo}\s+(\w+)'
            variaveis_funcao = re.findall(padrao_variavel_funcao, codigo_fonte)
            for nome_variavel in variaveis_funcao:
                tipo_variavel = None
                for tipo, nome_var in lista_variaveis:
                    if nome_var == nome_variavel:
                        tipo_variavel = tipo
                        if tipo_funcao != tipo_variavel:
                            # Verificar se o erro já foi registrado
                            erro = (nome_variavel, nome_funcao)
                            if erro not in erros:
                                erros.append(erro)
                                print(f"Erro semântico: O tipo da variável '{nome_variavel}' dentro da função '{nome_funcao}' não corresponde ao tipo da função.")
                        break
                    
    # Encontrar retornos de função
    padrao_retorno = r'\breturn\b\s*\((.+?)\)'
    returns = re.findall(padrao_retorno, codigo_fonte, re.MULTILINE | re.DOTALL)
    for i, retorno in enumerate(returns):
        tipo_retorno = None
        for tipo, nome in funcoes:
            if nome == lista_funcoes[i][1]:
                tipo_retorno = tipo
                break
        if tipo_retorno is not None:
            tipo_retorno_funcao = tipo_retorno.strip()
            tipo_retorno_retorno = retorno.strip()
            if tipo_retorno_funcao != tipo_retorno_retorno:
                print(f"Erro semântico: O tipo de retorno da função '{lista_funcoes[i][1]}' não corresponde ao tipo esperado.")

    # Verificar erros de chamadas de função
    padrao_chamada_funcao = r'(\w+)\s*\([^)]*\);'
    chamadas_funcao = re.findall(padrao_chamada_funcao, codigo_fonte)
    for nome in chamadas_funcao:
        if nome not in ['printf', 'scanf']:
            if nome not in [funcao[1] for funcao in funcoes]:
                if nome != 'return':
                    print(f"Erro semântico: Chamada para função '{nome}' não declarada.")

semantic_analysis()