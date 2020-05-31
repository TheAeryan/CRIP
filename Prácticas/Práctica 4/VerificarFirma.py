# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

Carlos Núñez Molina
Gabriela Antolinez
Alessandro Zito
"""

from GenerarClaves import *
from GenerarFirma import *
import hashlib as h


def verificacion_firma(m, r, s):
    w = potencia_modular(s, -1, q)
    mensaje_resumido = h.sha256(m)
    z = 0  # Aquí falta calcular z
    u = (z ** w) % q
    v = (r ** w) % q
    r1 = ((alfa ** u) * (y ** v) % p) % q
    if r == r1:
        print('Firma Valida!')
    else:
        print('La firma no es valida!')
