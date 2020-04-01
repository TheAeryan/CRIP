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
    x = 1<<n #x=2^m
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
Dado n un número compuesto, devuelve sus factores.
POR AHORA ESTOY SUPONIENDO QUE N ES PRODUCTO DE DOS PRIMOS!!!
"""
def factorizacion_fermat(n):
    x = math.ceil(math.sqrt(n)) # x empieza siendo ceil(sqrt(n))
    
    # Voy aumentando el valor de x hasta que encuentre una factorización
    while (True):
        y = x**2 - n
        
        if escuadrado(y): # Si y es un cuadrado, ya he encontrado los divisores de n
            r = raiz(y)
            
            # Devuelvo los dos divisores: (x-r) y (x+r)
            return (x-r, x+r)
        
        x += 1 # Incremento x en una unidad y vuelvo a probar
        
