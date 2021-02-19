# -*- coding: utf-8 -*-


"""
Dado un mensaje dar su codificación  usando el
algoritmo LZ78


mensaje='wabba wabba wabba wabba woo woo woo'
LZ78Code(mensaje)=[[0, 'w'], [0, 'a'], [0, 'b'], [3, 'a'], 
                   [0, ' '], [1, 'a'], [3, 'b'], [2, ' '], 
                   [6, 'b'], [4, ' '], [9, 'b'], [8, 'w'], 
                   [0, 'o'], [13, ' '], [1, 'o'], [14, 'w'], 
                   [13, 'o'], [0, 'EOF']]
"""

def LZ78Code(mensaje):
        diccionario = {'':0}
        codigo = []
        i = 0
        contador = 1
        while i < len(mensaje):
                simbolo_actual = ''
                while (simbolo_actual in diccionario) and i < len(mensaje):
                        simbolo_actual += mensaje[i]
                        i += 1

                if i > len(mensaje):
                            try:
                                index = diccionario[simbolo_actual]
                            except KeyError:
                                index = 0
                            codigo.append([index,'EOF'])
                            return codigo

                index = diccionario[simbolo_actual[:-1]]
                codigo.append([index,simbolo_actual[-1]])
                diccionario[simbolo_actual] = contador
                contador += 1
        codigo.append([0,'EOF'])
        return codigo

mensaje='mississippi mississippi river'
print(LZ78Code(mensaje))

"""
Dado un mensaje codificado con el algoritmo LZ78 hallar el mensaje 
correspondiente 

code=[[0, 'm'], [0, 'i'], [0, 's'], [3, 'i'], [3, 's'], 
      [2, 'p'], [0, 'p'], [2, ' '], [1, 'i'], [5, 'i'], 
      [10, 'p'], [7, 'i'], [0, ' '], [0, 'r'], [2, 'v'], 
      [0, 'e'], [14, 'EOF']]

print(" MISISIPI :",LZ78Decode(code))
   """ 

def LZ78Decode(codigo):
        mensaje = ''
        diccionario = ['']
        for i in codigo:
                if i[0] == 0:
                        if i[1] != 'EOF':
                                mensaje += i[1]
                                diccionario.append(i[1])
                else:
                        if i[1] != 'EOF': 
                            simbolo = diccionario[i[0]] + i[1]
                            mensaje += simbolo
                            diccionario.append(simbolo)
                        else:
                            simbolo = diccionario[i[0]]
                            mensaje += simbolo
                            diccionario.append(simbolo)
        return mensaje
"""

def LZ78Decode(codigo):
    output = ''
    table = []
    for index, character in codigo:
        if index == 0:
            if character != 'EOF':
                output += character
            table.append(character)
        else:
            substring = table[index - 1] + (character if character != 'EOF' else '')
            output += substring
            table.append(substring)
    return output
    """

mensaje='wabba wabba wabba wabba woo woo woo'  
mensaje_codificado=LZ78Code(mensaje)
print('Código: ',mensaje_codificado)   
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print('Código: ',mensaje_codificado)   
print(mensaje)
print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

mensaje='mississipi mississipi river' 
mensaje_codificado=LZ78Code(mensaje)
print('Código: ',mensaje_codificado)   
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print('Código: ',mensaje_codificado)   
print(mensaje)
print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

#%%
mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'

import time
bits_indice=12
start_time = time.clock()
mensaje_codificado=LZ78Code(mensaje)
print (time.clock() - start_time, "seconds CODE")
start_time = time.clock()
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print (time.clock() - start_time, "seconds DECODE")
ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
print(len(mensaje_codificado),ratio_compresion)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(len(mensaje),len(mensaje_recuperado))
        print(mensaje[-5:],mensaje_recuperado[-5:])

"""
print("--------LA REGENTA ENTERA--------")

with open ("la_regenta", "r") as myfile:
    mensaje=myfile.read()
print("long : ",len(mensaje))
mensaje_codificado=LZ78Code(mensaje)
mensaje_recuperado=LZ78Decode(mensaje_codificado)
ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
print(mensaje_recuperado[-200:])
print("")
print(mensaje == mensaje_recuperado)
print('Longitud de mensaje codificado:', len(mensaje_codificado))
print('Ratio de compresión:', ratio_compresion)


"""
print("----EXAMEN-----")
codigo = [[0, 'D'], [0, 'o'], [0, 'u'], [0, 'b'], [0, 'l'], [0, 'e'], [0, 't'], [0, 'h'], [0, 'i'], [0, 'n'], [0, 'k'], [0, ' '], [0, 'm'], [6, 'a'], [10, 's'], [12, 't'], [8, 'e'], [12, 'p'], [2, 'w'], [6, 'r'], [12, 'o'], [0, 'f'], [12, 'h'], [2, 'l'], [0, 'd'], [9, 'n'], [0, 'g'], [16, 'w'], [2, ' '], [0, 'c'], [2, 'n'], [7, 'r'], [0, 'a'], [25, 'i'], [30, 't'], [2, 'r'], [0, 'y'], [12, 'b'], [6, 'l'], [9, 'e'], [22, 's'], [12, 'i'], [10, ' '], [31, 'e'], [0, "'"], [0, 's'], [12, 'm'], [26, 'd'], [12, 's'], [9, 'm'], [3, 'l'], [7, 'a'], [10, 'e'], [2, 'u'], [46, 'l'], [37, ','], [12, 'a'], [10, 'd'], [57, 'c'], [30, 'e'], [0, 'p'], [7, 'i'], [10, 'g'], [38, 'o'], [7, 'h'], [21, 'f'], [16, 'h'], [6, 'm'], [0, '.'], [0, 'EOF']]

print(LZ78Decode(codigo))
