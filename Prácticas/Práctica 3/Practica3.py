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
import matplotlib.pyplot as trx
import numpy as np

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
def generar_compuestos_num_cifras(num_cifras, n=5): 
    lista_nums = []
    """
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
    """
    # Creo el resto de números compuestos
    while len(lista_nums) < n:
        x = randint(10**(num_cifras-1), 10**num_cifras)
        
        # Solo lo añado si es impar y compuesto
        if x % 2 == 1 and not test_MillerRabin(x, 20):
            lista_nums.append(x)
            
    return lista_nums

def generar_compuestos_num_cifras_primos(num_cifras): 
    lista_nums = []
    
    # Creo el compuesto como producto de primos
    num_cif_primos = num_cifras // 2
    
    # Elijo a dos primos aleatorios de num_cif_primos
    primos = []
    
    while len(primos) < 10:
        x = randint(10**(num_cif_primos-1), 10**num_cif_primos)
        
        # Compruebo si x es primo con el Test de Miller-Rabin con 20 testigos
        if test_MillerRabin(x, 20):
            primos.append(x)
            
    lista_nums.append(primos[0]*primos[1])
    lista_nums.append(primos[2]*primos[3])
    lista_nums.append(primos[4]*primos[5])
    lista_nums.append(primos[6]*primos[7])
    lista_nums.append(primos[8]*primos[9])
    
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

    # Veo primero si n es divisible por los primos más pequeños
    small_primes = [3,5,7]
    
    for p in small_primes:
        if n % p == 0:
            divisores = [p, n // p]
            
            # Compruebo si n // p es primo y, si no lo es, lo factorizo
            if not test_MillerRabin(divisores[1], 20):
                divisores[1] = factorizacion_pollard(divisores[1])

            return divisores
 
    p = raiz(n)
    while p:

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
            
            return divisores
                 
        #Si el mcd es 1, intento con otros numeros (la función f (x) que aumenta x y y es: f(x) = (x ** 2 + 1) mód n)
        x = (x ** 2 + 1) % n
        
        for i in range(2):
            y = (y ** 2 + 1) % n
        
        p -= 1


# ------------ Funciones para el logarítmo discreto -------------

def ld_fuerzabruta(a,b,p):
    for i in range(p-1):
        x=potencia_modular(a,i,p)
        if(x==b):
            return i
        if(x==1 and i!=0):
            return "No hay solución."

def ld_pasoenanogigante(a,b,p):

    s = raiz(p) + 1 
    sol = []
    #Pongo b en la lista
    sol.append(b % p)

    #Pongo todos los numeros desde b * a hasta b * (a ** (s - 1)) en la lista 
    for i in range(s-1):
        sol.append(sol[i] * a % p)

    #Ahora desde aquí vamos calculando n desde a ** s hasta a ** (s * s), y tenemos t como contador para ver hasta que no encontramos n = sol[i]
    n = (a ** s) % p
    t = 1
    while t != s:
        for i in range(len(sol)):
            if sol[i] == n:

                #Si lo encontramos, returnamos el resultado del logaritmo com t * s - i
                x = t * s - i
                return x
        n = (n * (a ** s)) % p
        t += 1
    print("No existe el numero")
    return

def ld_pollard(a,b,p):
    x,al,bet=[],[],[]
    x.append(1)
    al.append(0)
    bet.append(0)
    for i in range(30): 
        if x[i]%3==0:
            x.append((x[i]*x[i])%p)
            al.append((2*al[i])%(p-1))
            bet.append((2*bet[i])%(p-1))
        elif x[i]%3==1:
            x.append(x[i]*b%p)
            al.append(al[i])
            bet.append(bet[i]+1)
        else:    
            x.append(x[i]*a%p)
            al.append(al[i]+1)
            bet.append(bet[i])
        if i% 2 == 0: 
            x1=int(i/2)
            if x[i]==x[x1] and i!=0 : #Comparación entre i y 2i
                B,A=0,0
                B=bet[i]-bet[x1]  #Se genera la congruencia
                A=al[x1]-al[i]
                sol=congruencia(B,A,(p-1)) #Se soluciona la congruencia
                for i in range(len(sol)):
                    if (potencia_modular(a, sol[i], p))==b: #Se evaluan las posibles soluciones de la congruencia para el log
                        return sol[i]

# ------------ Funciones para el Análisis de Tiempo -------------

def analisis_tiempos_ldfuerza(lista1 = [[],[],[]]):
    tm = time.time()
    for i in range(len(lista1)):
        print(ld_fuerzabruta(lista1[i][0],lista1[i][1],lista1[i][2]))
        print(time.time() - tm)

def analisis_tiempos_ldpaso(lista1 = [[],[],[]]):
    tm = time.time()
    for i in range(len(lista1)):
        ld_pasoenanogigante(lista1[i][0],lista1[i][1],lista1[i][2])
        print(time.time() - tm)
        
def analisis_tiempos_ld_pollard(lista1 = [[],[],[]]):
	tm = time.time()
	for i in range(len(lista1)):
	    print(ld_pollard(lista1[i][0],lista1[i][1],lista1[i][2]))
	    print(time.time() - tm)
        
def analisis_tiempos_fb(lista1 = []):
    tm = time.time()
    for i in range(len(lista1)):
        factorizacion_tentativa(lista1[i])
    return (time.time() - tm) / 5



def analisis_tiempos_fermat(lista1 = []):
    tm = time.time()
    for i in range(len(lista1)):
        factorizacion_fermat(lista1[i])
    return (time.time() - tm) / 5



def analisis_tiempos_pollard(lista1 = []):
    tm = time.time()
    for i in range(len(lista1)):
        factorizacion_pollard(lista1[i])
    return (time.time() - tm) / 5


lista5 = [46191, 88369, 49651, 48159, 20609]
lista6 = [846979, 599721, 721071, 950975, 346295]
lista7 = [3239807, 2668751, 4868331, 6064247, 7183551]
lista8 = [46447573, 97961455, 61520637, 63582589, 37953139]
lista9 = [957589949, 285993255, 200223675, 993727427, 154075407]
lista10 = [3945148065, 2077524455, 1410741741, 3013455917, 7712733825]
lista15 = [913317468542225, 748978625210683, 211935444719693, 390393118631019, 575899868400667]
lista20 = [51604320814203832237, 63298031496990993641, 93152113314002488709, 82094134748542079777, 42668303529324435681]
lista25 = [5753781489398154520077575, 1568839284256802316822443, 1034216747782422372712111, 7204306301536692130224763, 4495855547372823594773827]


lista5_primos = [1577, 4757, 4559, 3071, 1007]
lista6_primos = [87847, 87271, 316159, 19511, 188561]
lista7_primos = [359893, 489347, 19879, 88163, 509017]
lista8_primos = [8241241, 29590747, 60880739, 35470933, 31341451]
lista9_primos = [34384457, 21894469, 8318159, 10381381, 52533491]
lista10_primos = [5826457841, 1791424123, 8435622953, 2990599379, 698162891]
lista15_primos = [70729893669023, 79693862188417, 11119413525721, 37723912694123, 27222054586633]
lista20_primos = [23832700531121320493, 32067152828622175193, 64838294355389912957, 77731138202499790837, 33423477292403677723]

#Los tiempos fuerza bruta no funcionan con numeros productos de primos de 20 cifras!
tiempos_fb_primos = [4.3010711669921876e-05, 5.3310394287109374e-05, 5.588531494140625e-05, 0.00019121170043945312, 0.0001750946044921875, 0.0022908687591552735, 0.25174527168273925]
tiempos_fb = [6.75201416015625e-05, 6.914138793945312e-05, 6.999969482421876e-05, 9.055137634277344e-05, 0.00010294914245605469, 0.00018744468688964845, 0.015476179122924805, 0.02575058937072754, 1.7505939483642579]

# Los tiempos fermat no funcionan con numeros de 10 cifras!
tiempos_fermat = [0.002565908432006836, 0.04211225509643555, 0.00943770408630371, 0.028308868408203125, 4.088871574401855, 99.91973805427551]
tiempos_fermat_primos = [0.0003816127777099609, 0.0009403228759765625, 0.0007202625274658203, 0.0013695716857910155, 0.0013250350952148438, 0.004761886596679687, 0.7187267303466797, 888.2101609230042]

#Los tiempos de pollard no funcionan con numeros
tiempos_pollard = []
tiempos_pollard_primos = []

