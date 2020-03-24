# -*- coding: utf-8 -*-

from Practica1 import *

# Elementos primitivos

def orden(a,n):
    i=1
    b = a
    while not b==1:
        b = (b*a)%n
        i+=1
    return i
        
def repetir_orden(n):
    for i in range(1, n):
        print(orden(i, n))

def es_primitivo(a,n):
    return orden(a,n) == n-1

def elementosprimitivos(n):
    sol = []
    for i in range(1,n-1):
        if es_primitivo(i,n):
            sol.append(i)
    return sol

# Devuelve true si a es primitivo
# Imprime todas las potencias a 
def primitivop1(a):
    div_primos = [2,3,7,19,2021879] # Factorización de p
    sol = True
    for i in div_primos:
        j = potencia_modular(a,6453837768//i,6453837769)
        print(j)
        sol = sol and not(j==1)
    return sol


    