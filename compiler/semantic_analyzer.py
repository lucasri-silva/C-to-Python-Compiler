import re

linhas_tratadas = []
errors = []
tokens = ['return','scanf']

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

# def semantic_analysis():
#     linhas_tratadas = codigo_fonte.split('\n')
#     padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
#     funcoes = re.findall(padrao_funcao, codigo_fonte)
#     funcoes_dict = {nome: tipo for tipo, nome in funcoes}

#     padrao_funcao_var = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{([^}]*)}'
#     funcoes = re.findall(padrao_funcao_var, codigo_fonte)
#     variaveis_retornos = {}
#     for tipo, nome, corpo in funcoes:
#         padrao_variavel = r'\b{}\b'.format(nome)
#         variaveis = re.findall(padrao_variavel, corpo)
#         variaveis_retornos[nome] = (tipo, variaveis)

#     print("\nEncontra erros semânticos no código: ")
#     cont=0
#     funcoes = re.findall(padrao_funcao_var, codigo_fonte)
#     for tipo, nome, corpo in funcoes:
#         padrao_variavel = r'(\w+)\s+(\w+)\s*;'
#         variaveis = re.findall(padrao_variavel, corpo)
#         for var_tipo, var_nome in variaveis:
#             if var_tipo != tipo:
#                 if (nome == 'main'):
#                     print("")
#                 else: 
#                     cont+=1
#                     print(f"A variável '{var_nome}' dentro da função '{nome}' retorna um valor de tipo diferente ({var_tipo} em vez de {tipo}).")


#     if cont == 0:
#         print("->não encontramos erros semánticos")

def semantic_analysis():
    print("Encontrando erros semânticos no código:")

    # Verificar erros de declaração de função
    padrao_funcao = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
    funcoes = re.findall(padrao_funcao, codigo_fonte)
    for tipo, nome in funcoes:
        if tipo not in ['void', 'int', 'float', 'double', 'char']:
            print(f"Erro semântico: Tipo de retorno inválido na função '{nome}'.")

    # Verificar erros de declaração de variáveis
    padrao_variavel = r'(\w+)\s+(\w+)\s*[,;=]'
    variaveis = re.findall(padrao_variavel, codigo_fonte)
    for tipo, nome in variaveis:
        if tipo not in ['void', 'int', 'float', 'double', 'char']:
            print(f"Erro semântico: Tipo de variável inválido na declaração de '{nome}'.")

    # Verificar erros de chamadas de função
    padrao_chamada_funcao = r'(\w+)\s*\([^)]*\);'
    chamadas_funcao = re.findall(padrao_chamada_funcao, codigo_fonte)
    for nome in chamadas_funcao:
        if nome not in ['printf', 'scanf']:
            if nome not in [funcao[1] for funcao in funcoes]:
                print(f"Erro semântico: Chamada para função '{nome}' não declarada.")
