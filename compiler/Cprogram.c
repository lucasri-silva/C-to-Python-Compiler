#include <stdio.h>

int somar (int a, int b) {
  return a;
}

int subtrair () {
  return (a-b);
}

int multiplicar (int a, int b) {
  return (a*b);
}

int dividir (int a, int b) {
  return (a/b);
}

int main(void) {
  int a = 10;
  int b = 2;
  scanf("%d",&a);
  scanf("%d",&b);
  int c = somar(a,b);
  int d = subtrair(a,b);
  int e = multiplicar();
  int f = dividir(a,b);
  printf("%d\n",a);
  printf("%d\n",d);
  printf("%d\n",e);
  printf("%d\n",f);
  return 0;
}