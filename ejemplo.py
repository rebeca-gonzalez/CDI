import math

def escribe(entrada, debug):
    if debug:
        print(entrada)


def blue(mensaje):
    return termcolor.colored(mensaje, 'blue')


def green(mensaje):
    return termcolor.colored(mensaje, 'green')


def red(mensaje):
    return termcolor.colored(mensaje, 'red')


def cdf(p):
    q = [
     0] * (len(p) + 1)
    for i in range(0, len(p)):
        q[i + 1] = q[i] + p[i]

    return q


def IntegerArithmeticCode(mensaje, alfabeto, frecuencias, numero_de_simbolos=1, debug=False):
    F = cdf(frecuencias)
    T = F[(-1)]
    n = len(mensaje)
    code = ''
    k = 2 + math.ceil(math.log(T + 1, 2))
    R = 2 ** k
    R2 = 2 ** (k - 1)
    m = 0
    M = R - 1
    if debug:
        print('Intervalo inicial: [' + str(m) + ',' + str(M) + ']')
    bits_acumulados = 0
    for i in range(0, n, numero_de_simbolos):
        letra = alfabeto.index(mensaje[i:i + numero_de_simbolos]) + 1
        if debug:
            antes = red('leo: ' + mensaje[i:i + numero_de_simbolos]) + ', ['
            for i_ in range(len(alfabeto)):
                antes = antes + str(m + math.floor((M - m + 1) * F[i_] / T)) + ' | '

            antes = antes + str(M) + ']'
        s = M - m + 1
        M = m + math.floor(s * F[letra] / T) - 1
        m = m + math.floor(s * F[(letra - 1)] / T)
        if debug:
            print(antes + red(', nuevo intervalo: [' + str(m) + ',' + str(M) + ']'))
        while True:
            if m >= R / 2:
                code_ = '1'
                M = 2 * M - R + 1
                m = 2 * m - R
                for _ in range(bits_acumulados):
                    code_ += '0'

                bits_acumulados = 0
                if debug:
                    print('Rescalado E2:')
                    print('codigo: ' + code + red(code_) + ', nuevo intervalo: [' + str(m) + ',' + str(M) + ']')
                code += code_
            elif M < R / 2:
                code_ = '0'
                M = 2 * M + 1
                m = 2 * m
                for _ in range(bits_acumulados):
                    code_ += '1'

                bits_acumulados = 0
                if debug:
                    print('Rescalado E1:')
                    print('codigo: ' + code + red(code_) + ', nuevo intervalo: [' + str(m) + ',' + str(M) + ']')
                code += code_
            elif m >= R / 4 and M < 3 * R / 4:
                M = 2 * M - R2 + 1
                m = 2 * m - R2
                bits_acumulados += 1
                if debug:
                    print('Rescalado E3:')
                    print('codigo: ......esperando...., bits_acumulados=' + str(bits_acumulados) + ', nuevo intervalo: [' + str(m) + ',' + str(M) + ']')
            else:
                break

    if debug:
        print('\n        Bits finales pendientes del rescalado:      \n        Al acabar el intervalo [m,M) no puede estar contenido en [0,R/2), ni en [R/4, 3R/4), ni en [R/2, R) por lo tanto [m,M) contiene R/4 y R/2 o R/2 y 3R/4. Para asegurarnos que enviamos un número del intervalo [m,M) en un caso enviamos 01.... y en el otro 10..... según m<=R/4 ó m>R/4\n        ')
    if m > R / 4:
        code_ = '10'
        for _ in range(bits_acumulados):
            code_ += '0'

        if debug:
            print('codigo: ' + code + red(code_))
        code += code_
    else:
        code_ = '01'
        for _ in range(bits_acumulados):
            code_ += '1'

        if debug:
            print('codigo: ' + code + red(code_))
        code += code_
    mb = bin(int(m))
    mb = mb[2:]
    mb = '0' * (k - len(mb)) + mb
    if debug:
        print('\n              Por último envío m representado por exactamente k bits\n              ')
        print(m, ' representado con exactamente ', k, ' bits:', mb)
        print('\nCodigo final: ' + code + red(mb))
    code += mb
    return code


def IntegerArithmeticDecode(codigo, tamanyo_mensaje, alfabeto, frecuencias, debug=False):
    F = cdf(frecuencias)
    T = F[(-1)]
    FF = []
    letra = 1
    for i in frecuencias:
        FF.extend([letra for _ in range(i)])
        letra = letra + 1

    mensaje = ''
    k = 2 + math.ceil(math.log(T + 1, 2))
    R = 2 ** k
    R2 = 2 ** (k - 1)
    m = 0
    M = R - 1
    x = 0
    for i in range(k):
        x = 2 * x + int(codigo[i])

    bit = k
    if debug:
        print('Número de bits para representar nuestros enteros:', k)
        print(red(codigo[:k]) + codigo[k:])
        print(x)
        print('\n')
    while bit < len(codigo):
        s = M - m + 1
        letra = FF[math.floor(((x - m + 1) * T - 1) / s)]
        if debug:
            antes = ''
            for aux in range(letra):
                antes = antes + str(m + math.floor(s * F[aux] / T)) + ' | '

            antes = antes + red(str(x)) + ' |' + str(m + math.floor(s * F[letra] / T) - 1) + '...' + str(M)
            print('\n Intervalo: ' + antes)
        mensaje += alfabeto[(letra - 1)]
        M = m + math.floor(s * F[letra] / T) - 1
        m = m + math.floor(s * F[(letra - 1)] / T)
        if debug:
            print(x)
            print('Símbolo: ', alfabeto[(letra - 1)])
            print('Mensaje: ', mensaje)
            despues = str(m) + ' | ' + red(str(x)) + ' | ' + str(M)
            print('Nuevo intervalo: ' + despues)
        while bit < len(codigo):
            if m >= R / 2:
                if debug:
                    antes = str(m) + ' <= ' + str(x) + ' < ' + str(M)
                M = 2 * M - R + 1
                m = 2 * m - R
                x = 2 * x - R + int(codigo[bit])
                bit += 1
                if debug:
                    despues = str(m) + ' <= ' + str(x) + ' < ' + str(M)
                    print('\nRescalado E_2: ' + antes)
                    print(codigo[:bit - 1] + ' ' + red(codigo[bit - 1:bit]) + ' ' + codigo[bit:])
                    print(antes + '------>' + despues)
            else:
                if M < R / 2:
                    if debug:
                        antes = str(m) + ' <= ' + str(x) + ' < ' + str(M)
                    M = 2 * M + 1
                    m = 2 * m
                    x = 2 * x + int(codigo[bit])
                    bit += 1
                    if debug:
                        despues = str(m) + ' <= ' + str(x) + ' < ' + str(M)
                        print('\nRescalado E_1: ' + antes)
                        print(codigo[:bit - 1] + ' ' + red(codigo[bit - 1:bit]) + ' ' + codigo[bit:])
                        print(antes + '------>' + despues)
                else:
                    if m >= R / 4 and M < 3 * R / 4:
                        if debug:
                            antes = str(m) + ' <= ' + str(x) + ' < ' + str(M)
                        M = 2 * M - R2 + 1
                        m = 2 * m - R2
                        x = 2 * x - R2 + int(codigo[bit])
                        bit += 1
                        if debug:
                            despues = str(m) + ' <= ' + str(x) + ' < ' + str(M)
                            print('\nRescalado E_3: ' + antes)
                            print(codigo[:bit - 1] + ' ' + red(codigo[bit - 1:bit]) + ' ' + codigo[bit:])
                            print(antes + '------>' + despues)
                    else:
                        break

    if debug:
        print('\nTemporal:', mensaje)
        print('Real:    ', mensaje[:tamanyo_mensaje])
    return mensaje[:tamanyo_mensaje]


lon_max = 30
print('Elige opción :')
print('( 0 ) Quit')
print('( 1 ) Codificación ejemplo de clase')
print('( 2 ) Decodificación ejemplo de clase')
print('( 3 ) Codificación ejemplo aleatorio paso a paso')
print('( 4 ) Codificación ejemplo aleatorio')
print('( 5 ) Decodificación ejemplo aleatorio paso a paso')
print('( 6 ) Decodificación ejemplo aleatorio')
opcion = int(input())
while opcion != 0:
    if opcion == 1:
        alfabeto = [
         'a', 'b', 'c', 'd']
        frecuencias = [1, 10, 20, 300]
        mensaje = 'dddcabccacabadac'
        print('\n\n\n')
        print(alfabeto)
        print(frecuencias)
        print(mensaje)
        print('\n\n\n')
        C = IntegerArithmeticCode(mensaje, alfabeto, frecuencias, numero_de_simbolos=1, debug=True)
        print(C, len(C), len(mensaje))
    else:
        if opcion == 2:
            alfabeto = [
             'a', 'b', 'c', 'd']
            frecuencias = [1, 10, 20, 300]
            mensaje = 'dddcabccacabadac'
            print('\n\n\n')
            print(alfabeto)
            print(frecuencias)
            print('\n\n\n')
            C = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)
            print(C, len(C), len(mensaje))
            mensaje_recuperado = IntegerArithmeticDecode(C, len(mensaje), alfabeto, frecuencias, False)
            print(mensaje == mensaje_recuperado)
        else:
            if opcion == 3:
                alfa = 'abcdefghijklmnopqrstuvwxyz'
                alfabeto = list(alfa[:random.randint(3, len(alfa))])
                frecuencias = [random.randint(1, 1000) for _ in alfabeto]
                indice = dict([(alfabeto[i], i + 1) for i in range(len(alfabeto))])
                U = ''
                for i in range(len(alfabeto)):
                    U = U + alfabeto[i] * frecuencias[i]

                def rd_choice(X, k=1):
                    Y = []
                    for _ in range(k):
                        Y += [random.choice(X)]

                    return Y


                n = random.randint(10, lon_max)
                L = rd_choice(U, n)
                mensaje = ''
                for x in L:
                    mensaje += x

                print('\n\n\n')
                print(alfabeto)
                print(frecuencias)
                print(mensaje)
                print('\n\n\n')
                C = IntegerArithmeticCode(mensaje, alfabeto, frecuencias, numero_de_simbolos=1, debug=True)
                print(C, len(C), len(mensaje))
            else:
                if opcion == 4:
                    alfa = 'abcdefghijklmnopqrstuvwxyz'
                    alfabeto = list(alfa[:random.randint(3, len(alfa))])
                    frecuencias = [random.randint(1, 1000) for _ in alfabeto]
                    indice = dict([(alfabeto[i], i + 1) for i in range(len(alfabeto))])
                    U = ''
                    for i in range(len(alfabeto)):
                        U = U + alfabeto[i] * frecuencias[i]

                    def rd_choice(X, k=1):
                        Y = []
                        for _ in range(k):
                            Y += [random.choice(X)]

                        return Y


                    n = random.randint(10, lon_max)
                    L = rd_choice(U, n)
                    mensaje = ''
                    for x in L:
                        mensaje += x

                    print('\n\n\n')
                    print(alfabeto)
                    print(frecuencias)
                    print(mensaje)
                    print('\n\n\n')
                    C = IntegerArithmeticCode(mensaje, alfabeto, frecuencias, numero_de_simbolos=1, debug=False)
                    print(C, len(C), len(mensaje))
                else:
                    if opcion == 5:
                        alfa = 'abcdefghijklmnopqrstuvwxyz'
                        alfabeto = list(alfa[:random.randint(3, len(alfa))])
                        frecuencias = [random.randint(1, 1000) for _ in alfabeto]
                        indice = dict([(alfabeto[i], i + 1) for i in range(len(alfabeto))])
                        U = ''
                        for i in range(len(alfabeto)):
                            U = U + alfabeto[i] * frecuencias[i]

                        def rd_choice(X, k=1):
                            Y = []
                            for _ in range(k):
                                Y += [random.choice(X)]

                            return Y


                        n = random.randint(10, lon_max)
                        L = rd_choice(U, n)
                        mensaje = ''
                        for x in L:
                            mensaje += x

                        print('\n\n\n')
                        print(alfabeto)
                        print(frecuencias)
                        print('\n\n\n')
                        C = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)
                        print(C, len(C), len(mensaje))
                        mensaje_recuperado = IntegerArithmeticDecode(C, len(mensaje), alfabeto, frecuencias, True)
                        print(mensaje == mensaje_recuperado)
                    else:
                        if opcion == 6:
                            alfa = 'abcdefghijklmnopqrstuvwxyz'
                            alfabeto = list(alfa[:random.randint(3, len(alfa))])
                            frecuencias = [random.randint(1, 1000) for _ in alfabeto]
                            indice = dict([(alfabeto[i], i + 1) for i in range(len(alfabeto))])
                            U = ''
                            for i in range(len(alfabeto)):
                                U = U + alfabeto[i] * frecuencias[i]

                            def rd_choice(X, k=1):
                                Y = []
                                for _ in range(k):
                                    Y += [random.choice(X)]

                                return Y


                            n = random.randint(10, lon_max)
                            L = rd_choice(U, n)
                            mensaje = ''
                            for x in L:
                                mensaje += x

                            print('\n\n\n')
                            print(alfabeto)
                            print(frecuencias)
                            print('\n\n\n')
                            C = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)
                            print(C, len(C), len(mensaje))
                            mensaje_recuperado = IntegerArithmeticDecode(C, len(mensaje), alfabeto, frecuencias, False)
                            print(mensaje == mensaje_recuperado)
                        else:
                            print('Opción no reconocida')
                        print('\n\n\nElige opción :')
                        print('( 0 ) Quit')
                        print('( 1 ) Codificación ejemplo de clase')
                        print('( 2 ) Decodificación ejemplo de clase')
                        print('( 3 ) Codificación ejemplo aleatorio paso a paso')
                        print('( 4 ) Codificación ejemplo aleatorio')
                        print('( 5 ) Decodificación ejemplo aleatorio paso a paso')
                        print('( 6 ) Decodificación ejemplo aleatorio')
                        opcion = int(input())
