#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Código asociado a la tercera práctica de Criptografía y Computación.

@author: Carlos Núñez Molina
@author: Alessandro Zito
@author: Gabriela Antolinez
"""

from Practica1 import *
import math
from random import randint
import time

# ------------ Funciones auxiliares ----------------

#Calcula el máximo común divisor de dos números.
def mcd(a,b):
    while b!=0:
        (a,b) = (b,a%b)
    return a

#Calcula el inverso de a módulo b (si existe). Si ni existe, lo dice y devuelve 0.
def inversomodular(a,b):
    (u0,u1) = (1,0)
    while b>0:
       (u0,u1) = (u1,u0-(a//b)*u1)
       (a,b) = (b,a%b)
    if a == 1:
       return u0
    else:
       print("No existe el inverso")
       return 0

#Resuelve la congruencia ax = b mod m. Da todas las soluciones comprendidas entre 0 y m-1.
def congruencia(a,b,m):
    d = mcd(a,m)
    if b%d == 0:
       n = m//d
       u = inversomodular(a//d,n)
       x = (u*(b//d))%n
       sol = []
       for i in range(d):
           sol.append(x)
           x += n
       return sol
    print("La congruencia no tiene solución")
    return([0])

#Calcula la raíz cuadrada entera de un número natural.
def raiz(n):    
    m = (len(bin(n))-1) // 2
    x = 1<<m #x=2^m
    y = (x**2+n)//(2*x)
    while x > y:
        (x,y) = (y,(y**2+n)//(2*y))
    return x

#Comprueba si un número natural es cuadrado perfecto.
def escuadrado(n):    
    y = raiz(n)
    return(y**2 == n)

# ------------ Funciones para la factorización -------------
      
"""
Genera una lista de n números compuestos de "num_cifras". Todos los números menos
uno se generan eligiendo un número impar al azar de num_cifras y comprobando que no es
primo. El otro número, se elige como múltiplo de dos números primos de num_cifras // 2. 
"""   
def generar_compuestos_num_cifras(num_cifras, n=10): 
    lista_nums = []
    
    # Creo el compuesto como producto de primos
    num_cif_primos = num_cifras // 2
    
    # Elijo a dos primos aleatorios de num_cif_primos
    primos = []
    
    while len(primos) < 2:
        x = randint(10**(num_cif_primos-1), 10**num_cif_primos)
        
        # Compruebo si x es primo con el Test de Miller-Rabin con 20 testigos
        if test_MillerRabin(x, 20):
            primos.append(x)
            
    lista_nums.append(primos[0]*primos[1])
    
    # Creo el resto de números compuestos
    while len(lista_nums) < n:
        x = randint(10**(num_cifras-1), 10**num_cifras)
        
        # Solo lo añado si es impar y compuesto
        if x % 2 == 1 and not test_MillerRabin(x, 20):
            lista_nums.append(x)
            
    return lista_nums
    
"""
Dado n un número compuesto, devuelve todos sus factores por fuerza bruta.
""" 
def factorizacion_tentativa(n):
    factores = []
    
    # Para poder "dar saltos" de 2 en 2 a través de todos los números impares,
    # primero saco los factores que son potencia de dos
    if n % 2 == 0:
        potencia = 1
        n = n // 2
            
        while n % 2 == 0:
            potencia += 1
            n = n // 2
        
        factores.append([2]*potencia)
        
    seguir = (n != 1) # Si n es potencia de 2, ya he terminado de factorizarlo
    
    x = 3
    
    while seguir:
        if n % x == 0: # X es divisor de n. Compruebo cuantas veces divide a n.
            potencia = 1
            n = n // x
            
            while n % x == 0:
                potencia += 1
                n = n // x
                
            # Añado el factor el número de veces necesario (según su potencia)
            factores.append([x]*potencia) # Se añade [x,x,x,...,x] donde el número de "x" es "potencia"
            
            # Si el número ya vale uno, he terminado de factorizarlo
            if n == 1:
                seguir = False
            # Si el número ya es primo, he terminado de factorizarlo
            elif test_MillerRabin(n, 20): # Aplico el Test de Miller-Rabin con 20 testigos
                factores.append([n]) # Añado al número primo como factor
                seguir = False
            
        x += 2 # Pruebo con el siguiente número impar
    
    return factores
    
"""
Dado n un número compuesto, devuelve todos sus factores usando el método de Fermat.
"""
def factorizacion_fermat(n):
    # Caso especial. Si n es cuadrado perfecto (n = a*a), entonces se factoriza
    # como a*a. Entonces hay que factorizar "a" si es necesario.
    if escuadrado(n):
        r = raiz(n)
        
        factores = [r, r]
        
        # Si son primos, los devuelvo. Si no, los vuelvo a factorizar recursivamente
        if not test_MillerRabin(r, 20):
            factores[0] = factores[1] = factorizacion_fermat(r)
            
        return factores
    
    x = raiz(n) + 1 # valor inicial de x
    
    # Voy aumentando el valor de x hasta que encuentre una factorización
    while (True):    
        y = x**2 - n

        if escuadrado(y): # Si y es un cuadrado, ya he encontrado los divisores de n
            r = raiz(y)
            
            # Los dos factores son (x-r) y (x+r)
            factores = [x-r, x+r]
            
            # Si son primos, los devuelvo. Si no, los vuelvo a factorizar recursivamente
            if not test_MillerRabin(factores[0], 20): # Uso el test de Miller-Rabin para comprobar primalidad con 20 testigos diferentes
                factores[0] = factorizacion_fermat(factores[0])
                
            if not test_MillerRabin(factores[1], 20):
                factores[1] = factorizacion_fermat(factores[1])
                
            return factores

        x += 1 # Incremento x en una unidad y vuelvo a probar


def factorizacion_pollard(n):

	x = 1
	y = 2
	
	start = time.clock()
	while True:
		a = mcd(y-x, n)

		#Si el MCD no es ni 1 ni n, entonces el numero que sale es divisor de n
		if a != 1 and a != n:

			#b será el otro divisor
			b = n // a
			divisores = [b, a]
			
			#Si son primos, los devuelvos. Si no, hago recursivamente la factorización.
			if not test_MillerRabin(divisores[0], 20):
				divisores[0] = factorizacion_pollard(divisores[0])

			if not test_MillerRabin(divisores[1], 20):
				divisores[1] = factorizacion_pollard(divisores[1])
			
			print(time.clock() - start)
			return divisores
		
		#Si el mcd es 1, intento con otros numeros (la función f (x) que aumenta x y y es: f(x) = (x ** 2 + 1) mód n)
		x = (x ** 2 + 1) % n
		
		for i in range(2):
			y = y ** 2 + 1
		y = y % n

			


# ------------ Funciones para el logarítmo discreto -------------

def ld_pasoenanogigante(a,b,p):
	s = raiz(p) + 1 
	sol = []
	sol.append(b % p)
	for i in range(s-1):
		sol.append(sol[i] * 11 % p)
	t = 1
	for t in range(s):
		n = (a ** (t * s)) % p
		for i in range(len(sol)):
			if sol[i] == n:
				x = t * s - i
				return x
	print("No existe el numero")
	return

