# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

@author: Carlos Núñez Molina
@author: Gabriela Antolinez
@author: Alessandro Zito
"""

import hashlib as h
from random import randint
from GenerarClaves import *
from Practica1 import *

def generacacion_firma(m):
    #Se hace el resumen del mensaje utilizando SHA-2.
    z = h.sha256(m)
    z=int(z.hexdigest(),16)
    #Se genera un número aleatorio de 2 a q-2.
    k = randint(2,q-2)
    #Se calcula la primera parte del par de la firma.
    r = (potencia_modular(alfa, k, p)) % q
    #Se calcula la segunda parte del par de la firma.
    s = ((z+x*r)*(pow (k,-1))) % q
    #Si r o s fuera igual a 0 se recalcula la firma.
    if (r==0 or s==0):
        generacacion_firma(m)
    else:
        nom_fich_firm = "firma.txt"
        with open(nom_fich_firm, 'w') as fich_firm:
            fich_firm.write(str(r) + '\n')
            fich_firm.write(str(s) + '\n')
        return r,s
    
