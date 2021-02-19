# -*- coding: utf-8 -*-
"""

"""

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, decidir si pueden definir un código.

'''

def  kraft1(L, q=2):
    suma = 0
    for i in L:
        suma += 1/q**i
    return (suma <= 1)


'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, calcular el máximo número de palabras de longitud 
máxima, max(L), que se pueden añadir y seguir siendo un código.

'''

def  kraft2(L, q=2):
    cont = 0
    Laux = L.copy()
    while( kraft1(Laux ,q)):
        Laux.append(max(Laux))
        cont += 1
    return cont


'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, calcular el máximo número de palabras 
de longitud Ln, que se pueden añadir y seguir siendo 
un código.
'''

def  kraft3(L, Ln, q=2):
    cont = 0
    Laux = L.copy()
    while( kraft1(Laux ,q)):
        Laux.append(Ln)
        cont += 1
    return cont


'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes

L=[2, 3, 3, 3, 4, 4, 4, 6]  
codigo binario (no es único): ['00', '010', '011', '100', '1010', '1011', '1100', '110100']

L=[1, 2, 2, 2, 3, 3, 5, 5, 5, 7]  
codigo ternario (no es único): ['0', '10', '11', '12', '200', '201', '20200', '20201', '20202', '2021000']
'''

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


#%%

'''
Ejemplos
'''
#%%

L=[2,3,3,3,4,4,4,6]
q=2

print("\n",sorted(L),' codigo final:',Code(L,q))
print(kraft1(L,q))
print(kraft2(L,q))
print(kraft3(L,max(L)+1,q))

#%%
q=3
L=[1,3,5,5,3,5,7,2,2,2]
print(sorted(L),' codigo final:',Code(L,q))
print(kraft1(L,q))


#%%
'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código CANÓNICO binario con palabras 
con dichas longitudes
'''

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
'''
Ejemplos
'''
#%%
L=[3, 3, 3, 3,3, 2, 4, 4]
C=CodeCanonico(L)
C==['010', '011', '100', '101', '110', '00', '1110', '1111']

#%%
L=[7,2,3,3,3,3,23,4,4,4,6]
C=CodeCanonico(L)
C==['1111010', '00', '010', '011', '100', '101', '11110110000000000000000', '1100', '1101', '1110', '111100']

print("-----EXAMEM------")
print("longitudes = [3,3,3,5,5,6,6,7,8,8,9,9,9]")
L=[3,3,3,5,5,6,6,7,8,8,9,9,9]
C=CodeCanonico(L)

print("codigo = ", C)

c = [3, 5, 3, 3, 5, 5]
print("canonico = ",CodeCanonico(c))