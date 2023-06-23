1: #include <stdio.h>
3: int somar (int a, float b) 
3: {
4: return (a+b);
5: }
7: int subtrair (int a, int b) 
7: {
8: return (a-b);
9: }
11: float multiplicar (int a, int b) 
11: {
12: return (a*b);
13: }
15: int dividir (int a, int b) 
15: {
16: return a/b;
17: }
19: int main(void) 
19: {
20: float a = 10;
21: int b = 2;
22: scanf("%f",&a);
23: scanf("%d",&b);
24: int c = somar(a,b);
25: int d = subtrair(a,b);
26: int e = multiplicar(a,x);
27: int f = dividir(a,b);
28: printf("%d\n",c);
29: printf("%d\n",a);
30: printf("%d\n",e);
31: printf("%d\n",f);
32: return 0;
33: }
