# -*- coding: utf-8 -*-
"""
@author: martinez
"""

import math
import random


'''
1. Definir una función Encode(M, m2c) que, dado un mensaje M y un diccionario 
de codificación m2c, devuelva el mensaje codificado C.
'''

''' RFC 1951 3.2.2'''

def Encode(M, m2c):
    C = ''
    i = 0
    while i < len(M):
        j = i + 1
        while j <= len(M):
            if M[i:j] in m2c:
                C += m2c[M[i:j]]
                i = j
                break
            j += 1
 
    return C

''' 
2. Definir una función Decode(C, c2m) que, dado un mensaje codificado C y un diccionario 
de decodificación c2m, devuelva el mensaje original M.
'''
def Decode(C,c2m):
    M = ''
    i = 0
    while i < len(C):
        j = i + 1
        while j <= len(C):
            if C[i:j] in c2m:
                M += c2m[C[i:j]]
                i = j
                break
            j += 1
    return M

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


def Code(L,q=2):
    Laux = sorted(L)
    codigo = []
    candidatos = ['']
    longitud = 0
    for i in Laux:
        while longitud < i:
            aux = []
            for x in candidatos:
                for j in range(q):
                    aux.append(x+str(j))
            candidatos = aux
            longitud += 1
        codigo.append(candidatos[0])
        candidatos.pop(0)
    return codigo


def CodeCanonico(L):
  Laux = Code(L)
  result = []
  for x in L:
    for i in range(len(Laux)):
      if (len(Laux[i]) == x):
        result.append(Laux[i])
        Laux.pop(i)
        break
  return result

#%%
"""
Dado un mensaje y su alfabeto con sus frecuencias dar un código 
que representa el mensaje utilizando precisión infinita (reescalado)

El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal 
que R>4T

T: suma total de frecuencias


alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
numero_de_simbolos=1
mensaje='ddddccaabbccaaccaabbaaddaacc' 
IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)=
'01011000111110000000000000000000001000010110001111000000000000000011011000000000000000000000001000010000000000000001000100010000000000010010100000010000'



alfabeto=['aa','bb','cc','dd']
frecuencias=[1,10,20,300]
numero_de_simbolos=2
mensaje='ddddccaabbccaaccaabbaaddaacc' 
IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)=
'0011010001100000000010000000000000010101000000000001000000001011111101001010100000'

"""


def IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos=1):
    codigo = ''
    cum_count = [0]
    T = 0
    for i in frecuencias:
            T += i
            cum_count.append(T)
    k = math.ceil(2+ math.log2(T))
    R = 2**k 

    l = 0
    u = R-1
    Scale3 = 0
    i = 0
    while(i < len(mensaje)):
        simbolo = ""
        for j in range(numero_de_simbolos):
            simbolo += mensaje[i+j]
        laux = l
        x = alfabeto.index(simbolo)+1
        l = laux + math.floor(((u - laux + 1)*cum_count[x - 1])/T) 
        u = laux + math.floor(((u - laux + 1)*cum_count[x]/T)) - 1
        MSB = ("{0:0" + str(k) + "b}").format(l)
        MSBl = MSB[0]
        MSB = ("{0:0" + str(k) + "b}").format(u)
        MSBu = MSB[0]
        while(MSBl == MSBu  or (l >= R/4 and u < R*3/4)):
            MSB = ("{0:0" + str(k) + "b}").format(l)
            MSBl = MSB[0]
            MSB = ("{0:0" + str(k) + "b}").format(u)
            MSBu = MSB[0]
            if(MSBl == MSBu):
                b = MSBl
                codigo +=b
                l = (l << 1)&((1 << k) - 1) 
                u = ((u << 1)&((1<<k) - 1))|1
                while(Scale3>0):
                    codigo += str(1-int(b))
                    Scale3 -= 1
            if(l >= R/4 and u < R*3/4):
                l = (l<<1)&((1<<k)-1) 
                u = ((u<<1)&((1<<k)-1))|1
                l ^= (1<<(k-1))
                u ^= (1<<(k-1))
                Scale3 += 1
        i+=numero_de_simbolos
    if Scale3 >0:
        if l < R/4:
            codigo += "01"
            for _ in range(Scale3):
                codigo +="1"
        else:
            codigo += "10"
            for _ in range(Scale3):
                codigo +="0"

    for i in range(k):
        aux = l&(1<<(k-1))
        l = l<<1
        codigo += str(aux >> (k-1))
    return codigo

alfabeto=['aa','bb','cc','dd']
frecuencias=[1,10,20,300]
numero_de_simbolos=2
mensaje='ddddccaabbccaaccaabbaaddaacc' 
codigo = IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)
print(codigo)
#%%
            
            
"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""
           
def IntegerArithmeticDecode(codigo,tamanyo_mensaje,alfabeto,frecuencias):
    cum_count = [0]
    T = 0
    for i in frecuencias:
            T += i
            cum_count.append(T)
    mensaje = ''
    k = math.ceil(2 + math.log2(T))
    R = 2 ** k
    l = 0
    u = R - 1
    t = 0
    for i in range(k):
        t = 2 * t + int(codigo[i])
    lectura = k
    while lectura < len(codigo):
        letra = math.floor(((t - l + 1) * T - 1) / (u - l + 1))
        index = 0
        end = False
        while not end and index < len(cum_count):
            if letra >= cum_count[index]:
                index += 1
            else:
                end = True
        letra = index 
        mensaje += alfabeto[(letra - 1)]
        uaux = u
        laux = l
        u = laux + math.floor(((uaux - laux + 1) * cum_count[letra]) / T) - 1
        l = laux + math.floor(((uaux - laux + 1) * cum_count[(letra - 1)] / T))
        while lectura < len(codigo) and not (l < R /2 and u >= R/2 and not (l >= R / 4 and u < 3 * R / 4)):
            if (l >= R / 2) or (u < R / 2):
                u = ((u << 1)&((1 << k) - 1))|1
                l = (l << 1)&((1 << k)-1) 
                t = (t << 1)&((1 << k)-1) | int(codigo[lectura])
                lectura += 1
            else:
                if l >= R / 4 and u < 3 * R / 4:
                    u = ((u << 1)&((1 << k) - 1))|1
                    l = (l << 1)&((1 << k)-1) 
                    t = (t << 1)&((1 << k)-1) | int(codigo[lectura])
                    lectura += 1
                    l = l^(1<<(k - 1))
                    u = u^(1<<(k - 1))
                    t = t^(1<<(k - 1))

    return mensaje[:tamanyo_mensaje]


alfabeto=['aa','bb','cc','dd']
frecuencias=[1,10,20,300]
numero_de_simbolos=2
mensaje='ddddccaabbccaaccaabbaaddaacc'
codigo = IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)
print()
print("IntegerArithmeticDecode: ",IntegerArithmeticDecode(codigo,len(mensaje),alfabeto,frecuencias))

#%%
'''
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''


def EncodeArithmetic(mensaje_a_codificar,numero_de_simbolos=1):
    dic = {}
    for i in range(0, len(mensaje_a_codificar), numero_de_simbolos):
        simbolo = ""
        for j in range(numero_de_simbolos):
            simbolo += mensaje_a_codificar[i+j]
        if simbolo not in dic:
            dic[simbolo] = 1
        else:
            dic[simbolo] += 1
    alfabeto = list(dic.keys())
    frecuencias = list(dic.values())
    mensaje_codificado = IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)
    return mensaje_codificado,alfabeto,frecuencias
    
def DecodeArithmetic(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias):
    mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias)
    return mensaje_decodificado
        
#%%
'''

Ejemplo (!El mismo mensaje se puede codificar con varios códigos¡)

'''

lista_C=['010001110110000000001000000111111000000100010000000000001100000010001111001100001000000',
         '01000111011000000000100000011111100000010001000000000000110000001000111100110000100000000']
alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
tamanyo_mensaje=len(mensaje)  

for C in lista_C:
    mensaje_recuperado=DecodeArithmetic(C,tamanyo_mensaje,alfabeto,frecuencias)
    print(mensaje==mensaje_recuperado)



#%%

'''
Ejemplo

'''

mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbelta torre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por un instinto de prudencia y armonía que modificaba las vulgares exageraciones de esta arquitectura. La vista no se fatigaba contemplando horas y horas aquel índice de piedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietan demasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sus segundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándose desde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones. Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegos malabares, en una punta de caliza se mantenía, cual imantada, una bola grande de bronce dorado, y encima otra más pequeña, y sobre ésta una cruz de hierro que acababa en pararrayos.'

mensaje_codificado,alfabeto,frecuencias=EncodeArithmetic(mensaje,numero_de_simbolos=1)
mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print(ratio_compresion)

if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!  ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


#%%

'''
Si no tenemos en cuenta la memoria necesaria para almacenar el alfabeto y 
las frecuencias, haced una estimación de la ratio de compresión para el 
fichero "la_regenta" que encontraréis en Atenea con numero_de_simbolos=1

Si tenemos en cuenta la memoria necesaria para almacenar el el alfabeto y 
las frecuencias, haced una estimación de la ratio de compresión.

Repetid las estimaciones con numero_de_simbolos=2,3,...
'''

with open ("la_regenta", "r") as myfile:
    mensaje=myfile.read()

        



#%%

'''
Comparad las ratios de compresión con las obtenidas con códigos de Huffman.
'''

        
