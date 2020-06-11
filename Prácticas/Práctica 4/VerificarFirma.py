# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

@author: Carlos Núñez Molina
@author: Gabriela Antolinez
@author: Alessandro Zito
"""

from hashlib import sha256
from Practica1 import *


def verificacion_firma(m):
    nom_fich_firma = "firma.txt"
    clave_priv = "clave_priv.txt"
    with open(nom_fich_firma, "r", encoding='utf-8-sig') as fich_firma:
        r = int(fich_firma.readline())
        s = int(fich_firma.readline())
        fich_firma.close()

    with open(clave_priv, "r", encoding='utf-8-sig') as f:
        p = int(f.readline())
        q = int(f.readline())
        alfa = int(f.readline())
        y = int(f.readline())
        f.close()

    w = potencia_modular(s, -1, q)

    # Utilizamos la función SHA2 importando haciendo el import de libreria 'hashlib', para tener el mensaje resumido
    z = sha256(m.encode())
    z = int(z.hexdigest(), 16)

    # Ahora calculamos u y v, dos parametros que necesitaremos para calcular la clave r1
    u = (z * w) % q
    v = (r * w) % q

    # r1 será nuestra clave que vamos a comparar con r del mensaje firmado
    r1 = ((alfa ** u) * (y ** v) % p) % q

    print(r1)

    # Si las claves son iguales, la firma será valida; si no, no será valido
    if r == r1:
        print('Firma Valida!')
    else:
        print('La firma no es valida!')
