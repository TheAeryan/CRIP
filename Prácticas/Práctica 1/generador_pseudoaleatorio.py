# -*- coding: utf-8 -*-

# Carlos Núñez Molina

# Generador Pseudoaleatorio
# El usuario introduce una cadena de caracteres a-z y es convertida a
# una cadena de 0 y 1

cadena_real = ""
        
# El usuario va introduciendo la cadena (puede ser en varias veces) hasta que
# introduce el caracter '$'

while True:
    nueva_cadena = input()
    
    if nueva_cadena == '$':
        break
    
    cadena_real = cadena_real + nueva_cadena
    
# Codifico los caracteres como 0 o 1: veo el número de su codificación ASCII
# y le hago módulo 2
    
cadena_codificada = ''.join([str(ord(i) % 2) for i in cadena_real])

print(cadena_codificada)