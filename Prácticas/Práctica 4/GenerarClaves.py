# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

@author: Carlos Núñez Molina
@author: Gabriela Antolinez
@author: Alessandro Zito
"""

from random import randint
from Practica1 import potencia_modular, test_MillerRabin, primo_de_longitud_n

# -- Primo q, de 256 bits --

Q = 256

q = primo_de_longitud_n(Q)

# -- Primo p, de 1024 bits. q debe ser divisor de p-1 --

L = 1024
C = L - Q  # Tamaño de c en bits

# Elijo a c como un número par al azar de C bits
c = randint(2 ** (C - 2), 2 ** (C - 1))
c *= 2

# Voy iterando sobre c hasta que p sea primo
p = c * q + 1

while not test_MillerRabin(p, 30):
    p += 2 * q

# -- Elemento alfa, que tenga orden q en Z_p --
# Como alfa tiene orden q, se cumple que alfa^q es congruente con 1 mod p
# Así, si elegimos alfa = g^((p-1)/q), alfa^q = g^(p-1) y por el Teorema de
# Fermat sabemos que eso vale 1, así que alfa^q vale 1.

g = randint(2, p - 2)
alfa = potencia_modular(g, (p - 1) // q, p)

# Si alfa vale 1, repito el proceso hasta que sea distinto de 1
while alfa == 1:
    g += 1
    alfa = potencia_modular(g, (p - 1) // q, p)

# -- Entero x, entre 2 y q-2 --   

x = randint(2, q - 2)

# -- Entero y, menor que p y que cumpla alfa^x congruente con y mod p -- 

y = potencia_modular(alfa, x, p)

# -- Genero los ficheros de clave pública y clave privada --

# Fichero clave pública: p, q, alfa, y
nom_fich_pub = "clave_pub.txt"

with open(nom_fich_pub, 'w') as fich_pub:
    fich_pub.write(str(p) + '\n')
    fich_pub.write(str(q) + '\n')
    fich_pub.write(str(alfa) + '\n')
    fich_pub.write(str(y))

# Fichero clave privada: p, q, alfa, y, x (¡contiene los parámetros de la clave pública!)
nom_fich_priv = "clave_priv.txt"

with open(nom_fich_priv, 'w') as fich_priv:
    fich_priv.write(str(p) + '\n')
    fich_priv.write(str(q) + '\n')
    fich_priv.write(str(alfa) + '\n')
    fich_priv.write(str(y) + '\n')
    fich_priv.write(str(x))
