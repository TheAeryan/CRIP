# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

@author: Carlos Núñez Molina
@author: Gabriela Antolinez
@author: Alessandro Zito
"""

from hashlib import sha256
from Practica1 import *
from Practica3 import inversomodular


def verificacion_firma(mensaje):

    # Leemos el mensaje en binario y lo convertimos a entero (la variable mensaje sería el nombre de un cualquier
    # fichero (pdf, txt, ecc...)
    z = sha256(open(mensaje, "rb").read()).hexdigest()
    z = int(z, 16)

    nom_fich_firma = "firma.txt"
    clave_pub = "clave_pub.txt"

    # Leemos los par de claves de la firma
    with open(nom_fich_firma, "r", encoding='utf-8-sig') as fich_firma:
        r = int(fich_firma.readline())
        s = int(fich_firma.readline())
        fich_firma.close()

    # Leemos las claves generadas para firmar
    with open(clave_pub, "r", encoding='utf-8-sig') as f:
        p = int(f.readline())
        q = int(f.readline())
        alfa = int(f.readline())
        y = int(f.readline())
        f.close()

    w = inversomodular(s, q)

    # Ahora calculamos u y v, dos parametros que necesitaremos para calcular la clave r1
    u = (z * w) % q
    v = (r * w) % q

    # r1 será nuestra clave que vamos a comparar con r del mensaje firmado
    r1 = ((potencia_modular(alfa, u, p) * potencia_modular(y, v, p)) % p) % q

    # Si las claves son iguales, la firma será valida; si no, no será valido
    if r == r1:
        print('Firma vValida!')
    else:
        print('La firma no es valida!')
