#include <stdio.h>

int somar (int a, float b) {
  return (a+b);
}

int subtrair (int a, int b) {
  return (a-b);
}

float multiplicar (int a, int b) {
  return (a*b);
}

int dividir (int a, int b) {
  return a/b;
}

int main(void) {
  float a = 10;
  int b = 2;
  scanf("%f",&a);
  scanf("%d",&b);
  int c = somar(a,b);
  int d = subtrair(a,b);
  int e = multiplicar(a,x);
  int f = dividir(a,b);
  printf("%d\n",c);
  printf("%d\n",a);
  printf("%d\n",e);
  printf("%d\n",f);
  return 0;
  }
