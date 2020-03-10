abecedario = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']



#Dado un texto (string) solo con mayusculas lo transforma en una lista de números (A-0,...,Z-26). Por un espacio añade un -1

def cadenatolista(cadena):
    l = []
    for s in cadena:
        x = ord(s)
        if x == 32:
            l.append(-1)
        elif x < 79:
            l.append(x-65)
        elif x == 209:
            l.append(14)
        else:
            l.append(x-64)
    return l

#Inverso del anterior. Una lista de números (0--26) lo transforma en un string con mayúsculas
def listatocadena(l):
    s = ''
    for x in l:
        if x == -1:
            s = s + ' '
        elif x <= 13:
            s = s + chr(x+65)
        elif x == 14:
            s = s + 'Ñ'
        else:
            s = s + chr(x+64)
    return s


#Calcula las frecuencias de aparición de cada letra en una cadena de texto (en mayúsculas)

def frecuencias(texto):
    tabla = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    N = len(texto)
    lista = cadenatolista(texto)
    for x in lista:
        tabla[x] = tabla[x]+1
    for i in range(27):
        tabla[i] = (tabla[i]*100000//N)/1000
    sol = sorted(list(zip(tabla,abecedario)))
    sol.reverse()
    return sol


#Calcula el indice de coincidencia de un texto.
def indice_coincidencia(texto):
    tabla = frecuencias(texto)
    num_caracteres = 0
    aux = 0
    for x in tabla:
        num_caracteres +=x
        aux = aux + x*(x-1)
    ic = aux/(num_caracteres*(num_caracteres-1))
    return ic


#Divide un texto en n subtextos, recorriéndolo de n en n.
def divide_cadena(cadena,n):
     subcadenas = []
     for i in range(n):
         subcadenas.append('')
     j = 0
     for x in cadena:
         subcadenas[j] = subcadenas[j] + x
         j = (j+1)%n
     return subcadenas


#Dado un texto y una clave  (ambos un string con mayúsculas), lo cifra usando el cifrado de Vigenère
def cifra_vigenere(texto,clave):
     lista_texto = cadenatolista(texto)
     lista_clave = cadenatolista(clave)
     (n,m) = (len(lista_texto),len(lista_clave))
     for i in range(n):
          lista_texto[i] = (lista_texto[i] + lista_clave[i%m])%27
     texto_cifrado = listatocadena(lista_texto)
     return texto_cifrado


"""Dado un texto y una permutación de las letras (diccionario) lo cifra aplicando la sustitución dada
La sustitución hay que darla como un diccionario. Por ejemplo:
sustitucion = {'A':'B', 'B':'C', 'C':'D', 'D':'E', 'E':'F', 'F':'G', 'G':'H', 'H':'I', 'I':'J', 'J':'K', 'K':'L', 'L':'M', 'M':'N', 'N':'Ñ', 'Ñ':'O', 'O':'P', 'P':'Q', 'Q':'R', 'R':'S', 'S':'T', 'T':'U', 'U':'V', 'V':'W', 'W':'X', 'X':'Y', 'Y':'Z', 'Z':'A'}
que sustituye cada carácter por el que le sigue en el alfabeto
"""
def cifra_sustitucion(texto,permutacion):
     texto_cifrado = ''
     for x in texto:
         y = permutacion.get(x)
         texto_cifrado = texto_cifrado + y
     return texto_cifrado

"""permutación es una lista de dos strings (de igual longitud). Por ejemplo, ['AEG',fkl']. En este caso, se recorre el texto y cada vez que encuentre un carácter que coincida con un de los que hay en 'AEG' lo sustituye por el correspondiente carácter en 'fkl'"""
def descifra_sustitucion(texto,permutacion):
     texto_des = ''
     p0 = permutacion[0]
     p1 = permutacion[1]
     for x in texto:
         if x in p0:
              pos = p0.index(x)
              texto_des = texto_des + p1[pos]
         else:
              texto_des = texto_des + x
     return texto_des 


#En un texto selecciona los m n-gramas que más se repiten (m=5 por defecto) y da la frecuencia de aparición de cada uno de ellos.
def ngramas_repetidos(texto,n,m=5):
    ngramas = []
    ngramasrep = []
    frecuencias = []
    for i in range(m):
        frecuencias.append(0)
        ngramasrep.append(texto[i:i+n])
    minimo = 0
    for i in range(len(texto)-n):
         aux = texto[i:i+n]
         if aux not in ngramas:
             f = 1
             ngramas.append(aux)
             for j in range(i+1,len(texto)-n):
                 if aux == texto[j:j+n]:
                     f+=1
             if f > minimo:
                 k = frecuencias.index(minimo)
                 ngramasrep[k] = aux
                 frecuencias[k] = f
                 minimo = min(frecuencias)
    return (ngramasrep,frecuencias)



#Dada una cadena y un texto calcula las veces en que aparece la cadena, y la separación entre estas apariciones.
def apariciones(cadena,texto):
    m = len(cadena)
    n = len(texto)
    posicion = []
    for i in range(n-m):
        if cadena == texto[i:i+m]:
            posicion.append(i)
    return (posicion,len(posicion))
     


#Recorre el texto de n en n, comenzando por la primera posición. Al llegar al final, comienza por la segunda posición y así sucesivamente. 
def descifra_transposicion(texto,n):
     m = len(texto)
     k = m%n
     texto_cif = ''
     for i in range(n):
         if i < k:
             aux = m//n+1
         else: 
             aux = m//n
         for j in range(aux):
             texto_cif = texto_cif + texto[i+n*j]
     return texto_cif

#Suponiendo que se ha recorrido de n en n un texto de tamaño m, nos dice en que posición estaría el carácter siguiente al que está en la posición x. Primero calculamos donde estaría el último, pues ese no tiene siguiente.
def siguiente(m,n,x):
     aux = m%n
     aux2 = m//n
     if aux == 0:
         ultimo = -1
     else: 
         ultimo = aux * (aux2 + 1) - 1
     if ultimo == -1 and x == m-1:
         return -1
     elif x < ultimo:
         return x+1+aux2
     elif x >= m - aux2:
         return x + aux2 + 1 - m
     elif x > ultimo:
         return x+aux2
     else:
         return -1

def cifra_transposicion(texto,n):
    m = len(texto)
    texto_des = ''
    j = 0
    for i in range(m):
        texto_des = texto_des + texto[j]
        j = siguiente(m,n,j)
    return texto_des


#Cuenta cuantas veces se repite una cadena en el fichero texto suponiendo que éste se ha obtenido recorriendo un fichero de n en n.
def ocurrencias(cadena,texto,n):
     l = len(texto)
     k = len(cadena)
     ocur = 0
     for i in range(l):
          contador = i
          cadenab = ''
          for j in range(k):
              if contador == -1:
                    cadenab = cadenab + ' '
                    contador = 0
              else:
                    cadenab = cadenab + texto[contador]
                    contador = siguiente(l,n,contador)
          if cadena == cadenab:
              ocur +=1
     return ocur
          
  
