# -*- coding: utf-8 -*-


'''
0. Dada una codificación R, construir un diccionario para codificar m2c y 
otro para decodificar c2m
'''
R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])


'''
1. Definir una función Encode(M, m2c) que, dado un mensaje M y un diccionario 
de codificación m2c, devuelva el mensaje codificado C.
'''

''' RFC 1951 3.2.2'''

def keyEncode(key):
    return key == m2c[0] or key == m2c[1] or key == m2c[2] or key == m2c[3] or key == m2c[4]

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
  
#%%
#------------------------------------------------------------------------
# Ejemplo 1
#------------------------------------------------------------------------

R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

M='aabacddeae'
C=Encode(M,m2c)
C=='0011010010101010101101011'
M==Decode(C,c2m)



#%%
#------------------------------------------------------------------------
# Ejemplo 2
#------------------------------------------------------------------------
R = [('a','0'), ('b','10'), ('c','110'), ('d','1110'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])
M='aabacddeaeabc'
C=Encode(M,m2c)
C=='0010011011101110111101111010110'
M==Decode(C,c2m)



#%%
#------------------------------------------------------------------------
# Ejemplo 3
#------------------------------------------------------------------------
import random

R = [('ab','0'), ('cb','11'), ('cc','100'), ('da','1010'), ('ae','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in m2c.items()])

M='ababcbccdaae'
C=Encode(M,m2c)
C=='001110010101011'
M==Decode(C,c2m)


''' 
3.
Codificar y decodificar 20 mensajes aleatorios de longitudes también aleatorias.  
Comprobar si los mensajes decodificados coinciden con los originales.
'''

def mensajesRandom():
    for i in range(20):
        rand = random.randint(10000,1000000)
        M = ""
        for j in range(rand):
            M += random.choice(list(m2c))
        C=Encode(M,m2c)
        print(M==Decode(C,c2m))        

mensajesRandom()

#%%
#------------------------------------------------------------------------
# Ejemplo 4
#------------------------------------------------------------------------
R = [('a','0'), ('b','01'), ('c','011'), ('d','0111'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])



''' 
4. Codificar y decodificar los mensajes  'ae' y 'be'. 
Comprobar si los mensajes decodificados coinciden con los originales.
'''

M1='ae'
M2='be'
C1=Encode(M1,m2c)
print(C1)
print(M1==Decode(C1,c2m))
C2=Encode(M2,m2c)
print(C2)
print(M2==Decode(C2,c2m))



'''
¿Por qué da error?
El codigo R no es prefijo, por tanto hay incertidumbre a la hora de decodificar
(No es necesario volver a implementar Decode(C, m2c) para que no dé error)
'''



  




