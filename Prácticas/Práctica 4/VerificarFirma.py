# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

@author: Carlos Núñez Molina
@author: Gabriela Antolinez
@author: Alessandro Zito
"""

import hashlib as h
from GenerarClaves import *


def verificacion_firma(m, r, s):
    w = potencia_modular(s, -1, q)

    # Utilizamos la función SHA2 importando haciendo el import de libreria 'hashlib'
    mensaje_resumido = h.sha256(m)

    # Cogemos los primeros Q bits del mensaje resumido
    z = mensaje_resumido >> Q

    # Ahora calculamos u y v, dos parametros que necesitaremos para calcular la clave r1
    u = (z * w) % q
    v = (r * w) % q

    # r1 será nuestra clave que vamos a comparar con r del mensaje firmado
    r1 = ((alfa ** u) * (y ** v) % p) % q

    # Si las claves son iguales, la firma será valida; si no, no será valido
    if r == r1:
        print('Firma Valida!')
    else:
        print('La firma no es valida!')
