#include <stdio.h>

int somar (int a, int b) {
  int x = 10;
  return a;
}

int subtrair (int a, int b) {
  return 10;
}

int multiplicar (int a, int b) {
  return (a*b);}

int dividir (int a, int b) {
  return (a/b);}

int main() {
  int a = 10;
  int b = 2;
  scanf("%d",&a);
  scanf("%d",&b);
  int c = somar(a,b);
  int d = subtrair(a,b);
  int e = multiplicar(a,b);
  int f = dividir(a,b);
  printf("%d\n",a);
  printf("%d\n",d);
  printf("%d\n",e);
  printf("%d\n",f);
  return 0;}