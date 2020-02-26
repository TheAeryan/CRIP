#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Calcular a^b mod m

import sys
import time
from random import randint

# Naive
# Es O(b)
def potencia_modular_naive(a, b, m):
	res = 1

	for i in range(b):
		res *= a

		res = res % m
	
	return res;

# Ahorra en el número de potencias   
# Ej.: si es 7^100 mod m, 7^100 es 7^64 * 7^32 * 7^4. Lo hago así
# para ahorrar multiplicaciones (esa descomposición viene dada
# por las cifras donde el número en binario vale 1)
# Es O(log(b))
def potencia_modular(a, b, m):
    p = 1
    
    while b > 0:
        
        # Veo si la última cifra del número en binario vale 1
        if b % 2 == 1:
            p = (p*a) % m # "Cojo" esa potencia
            
        b = b >> 1 # Desplazo un bit (cifra en binario)
        
        a = (a*a) % m # Siguiente potencia
        
    return p

# Test de Fermat
# Es p primo?
# 1. Elegimos a tq. 2 <= a <= p-2
# 2. b = a^p-1 mod p
# 3. Si b != 1, p no es primo. Si b = 1, p es <probable> primo.
def test_fermat_repetido(p):
    num_rep = 100
    
    for i in range(num_rep):
        a = randint(2, p-2) # Elegimos aleatoriamente la base del exponente
        
        print(potencia_modular(a, p-1, p))
    
# Obtiene las raíces de la ecuación congruencial x^2 - 1 = 0 mod p
# Si para p esta ecuación tiene más de dos soluciones p no es primo.
# Si solo tiene dos soluciones, p puede ser primo
        
# Como mínimo, siempre son soluciones de la ecuación (raíces): 1 y p-1
# Por esto, ver si la ecuación tiene más de dos raíces se reduce a ver
# si hay algún otro número distinto de 1 y n-1 que sea solución
def raicesuno(p):
    l = []
    
    for i in range(1, p):
        if (i*i) % p == 1:
            l.append(i)
            
    return l

def raicesunorep():
    
    for j in range(2, 100):
        print(j, raicesuno(j))

# Si p es primo
# a^(p-1) = 1 mod p
# x² - 1 = 0 mod p tiene dos soluciones
# El test de Miller-Rabin  usa estas dos ideas para comprobar si un número es primo
        
# Tenemos n que queremos ver si es primo y a es un testigo (2<=a<=n-2)
# 1. Descomponemos n-1 como 2^u*s (s impar)
# 2. Calculamos a = a^s mod n
# 3. Si a = 1 o a = n-1 -> n es probable primo (Si a=1, al ir iterando y calculando a, siempre va a valer a y de forma parecida pasa cuando vale n-1)
# 4. Desde i=1 hasta u-1
#   a = a^2 mod n
#   si a = 1 -> n no es primo
#   si a = n-1 -> n es probable primo

# El número de testigos falsos es como mucho un cuarto del número
# total de testigos -> Este test falla (da resultado de probable
# primo cuando no lo es), como mucho un 25% de las veces

# Paso 1
def descomponer_2us(n_m1):
    a = n_m1
    u = 0
    
    while a % 2 == 0:
        a = a // 2
        u += 1
        
    return u, a

# Devuelve True si n pasa la prueba (es probable primo)
def test_MillerRabin_unavez(n, a):
    # Paso 1
    u, s = descomponer_2us(n-1)
    
    # Paso 2
    a = potencia_modular(a, s, n)
    
    # Paso 3
    if a == 1 or a == n-1:
        return True
    else:
        for i in range(1, u): # El último caso se corresponde siempre con el Test de Fermat
            a = potencia_modular(a,2,n)
            
            if a == 1:
                return False
            
            # Si a vale n-1, eso en módulo n es igual a -1
            # Así, al elevarlo al cuadrado siempre me dará 1
            # De esta forma, solo me salen como solución de la ecuación
            # 1 y n-1, con lo que n es probable primo
            if a == n-1:
                return True

        return False


# <Funciones de la práctica>
# Dado n, m
# Elige m testigos al azar (entre 2 y n-2)
# Comprueba si n es probable primo o no
def test_MillerRabin(n, m):
    
    for i in range(m):
        a = randint(2, n-2) # Testigo
        
        res = test_MillerRabin_unavez(n, a)
        
        if not res:
            return False # Ya sé que no es primo
        
    return True

# Dado n, elige el primer primo p>=n
# (voy sumandole dos hasta encontrar un probable primo) 
def primer_primo_mayor(n):
    num_rep = 20 # Probabilidad menor a 1 entre un billón
    
    if n % 2 == 0:
        n += 1
    
    es_pos_primo = False
    
    n = n-2
    while not es_pos_primo:
        n += 2
        es_pos_primo = test_MillerRabin(n, num_rep)
      
    return n

# Dado n, elige el primer primo fuerte p>=n
# Primo fuerte: si p como (p-1)/2 es primo
def primer_primo_fuerte_mayor(n):
    num_rep = 20 # Probabilidad menor a 1 entre un billón
    
    if n % 2 == 0:
        n += 1
    
    es_pos_primo_fuerte = False
    
    n = n-2
    while not es_pos_primo_fuerte:
        n += 2
        es_pos_primo = test_MillerRabin(n, num_rep)
        
        # Si es posible primo, veo si (p-1)/2 también lo es
        if es_pos_primo:
            es_pos_primo_fuerte = test_MillerRabin((n-1)//2, num_rep)
      
    return n
    
# Dado n, devuelve un primo de n bits
# p debe estar entre 2^n-1 y 2^n -> Elegir aleatorio en ese rango y calcular siguiente primo
def primo_de_longitud_n(n):
    # Elijo un random int entre 2^n-1 y 2^n
    ini = randint(2**(n-1), 2**n)
    
    # Calculo el siguiente primo
    p = primer_primo_mayor(ini)
    
    return p

# Dado n, devuelve un primo fuerte de n bits
def primo_fuerte_de_longitud_n(n):
    # Elijo un random int entre 2^n-1 y 2^n
    ini = randint(2**(n-1), 2**n)
    
    # Calculo el siguiente primo fuerte
    p = primer_primo_fuerte_mayor(ini)
    
    return p



# En la memoria no hay que escribir mucho, solo hay que poner los resultados:
# Ej: n no es primo porque es producto de a*b*c y me han salido en esta función tantos testigos falsos

# Primo grande -> 10 cifras por ejemplo (elegido con nuestra función de siguiente primo)

# No es necesario hacer main
