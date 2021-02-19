# -*- coding: utf-8 -*-
"""

"""
import math
import numpy as np
import matplotlib.pyplot as plt


'''
Dada una lista p, decidir si es una distribución de probabilidad (ddp)
0<=p[i]<=1, sum(p[i])=1.
'''
def es_ddp(p,tolerancia=10**(-5)):
    suma = 0
    for i in p:
        suma += i
        if ( i < 0 or i > 1): return False
    if( suma > 1+tolerancia or suma < 1-tolerancia): return False
    return True


'''
Dado un código C y una ddp p, hallar la longitud media del código.
'''

def LongitudMedia(C,p):
    suma = 0
    n = len(C)
    for i in range(n):
        tam = len(C[i])
        suma += tam * p[i]
    return suma

    
'''
Dada una ddp p, hallar su entropía.
'''
def H1(p):
    entropia = 0
    for i in range (len(p)):
        if (p[i] != 0):
            entropia += p[i] * math.log(1/p[i],2)
    return entropia


'''
Dada una lista de frecuencias n, hallar su entropía.
'''
def H2(n):
    longitud = sum(n)
    ddp = [x/longitud for x in n]
    return H1(ddp)



'''
Ejemplos
'''
C=['001','101','11','0001','000000001','0001','0000000000']
p=[0.5,0.1,0.1,0.1,0.1,0.1,0]
n=[5,2,1,1,1]

print("es_ddp ",es_ddp(p))
print(H1(p))
print(H2(n))
print(LongitudMedia(C,p))


'''
Dibujar H([p,1-p])
'''
lista = [x/100 for x in range(101)]
print(lista)
lista2 = [lista[100-x] for x in range(101)]
print(lista2)

plt.plot(lista, [H2([lista[x], lista2[x]]) for x in range (101)])
plt.show()






