# -*- coding: utf-8 -*-

"""
Práctica 4 de Criptografía - Firma Digital

@author: Carlos Núñez Molina
@author: Gabriela Antolinez
@author: Alessandro Zito
"""

from hashlib import sha256
from random import randint
from GenerarClaves import *
from Practica1 import *
from Practica3 import inversomodular


def generacion_firma(mensaje):

    # Se lee el fichero.

    clave_priv = "clave_priv.txt"
    with open(clave_priv, "r", encoding='utf-8-sig') as f:
        p = int(f.readline())
        q = int(f.readline())
        alfa = int(f.readline())
        y = int(f.readline())
        x = int(f.readline())

    # Se hace el resumen del mensaje utilizando SHA-2 y se convierte el resumen a decimal para que se puedan utilizar
    # diversas operaciones en el.

    z = sha256(open(mensaje, "rb").read()).hexdigest()
    z = int(z, 16)

    # Se genera un número aleatorio de 2 a q-2.
    k = randint(2, q - 2)

    # Se calcula la primera parte del par de la firma.
    r = (potencia_modular(alfa, k, p)) % q

    # Se calcula la segunda parte del par de la firma con la función invernomodular(a, b)
    s = ((z + x * r) * inversomodular(k, q)) % q

    # Si r o s fuera igual a 0 se recalcula la firma.
    if r == 0 or s == 0:
        generacion_firma(mensaje)
    else:
        nom_fich_firm = "firma.txt"
        with open(nom_fich_firm, 'w') as fich_firm:
            fich_firm.write(str(r) + '\n')
            fich_firm.write(str(s) + '\n')
            fich_firm.close()
