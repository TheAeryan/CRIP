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
        x1=potencia_modular(b,1,p)
        x=potencia_modular(a,i,p)
        if(x==x1):
            return i
        if(x1==1 and i!=0):
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
    aux = a ** s
    n = aux % p #UTILIZAR POTENCIA MODULAR
    t = 1
    while t != s:
        for i in range(len(sol)):
            if sol[i] == n:

                #Si lo encontramos, returnamos el resultado del logaritmo com t * s - i
                x = t * s - i
                return x
        n = n * (aux) % p #UTILIZZARE ALTRA VARIABILE
        t += 1
    print("No existe el numero")
    return

def ld_pollard(a,b,p):
    x,al,bet=[],[],[]
    x.append(1)
    al.append(0)
    bet.append(0)
    for i in range(p-1): 
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
                    bo=potencia_modular(b,1,p)
                    if (potencia_modular(a, sol[i], p))==bo: #Se evaluan las posibles soluciones de la congruencia para el log
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
lista=[5,2,7],[61,34,47],[320,240,193],[4320,7240,1613],[53205,62407,39581],[753205,853407,465901],[8753209,1853401,6561437],[18753208,61853403,15484247],[238763200,751803489,957833221],[9238763200,8751803410,2111511013]        

tiempo_ldfuerza=[0.002000093460083008,0.009000301361083984,0.016000032424926758,0.025000333786010742,0.12840008735656738,3.954200029373169,25.077800273895264,97.6502001285553]
tiempo_ldpaso=[0.015599966049194336,0.015599966049194336,0.015599966049194336,0.031200170516967773,0.031200170516967773,0.07800006866455078,0.32760000228881836,0.9828000068664551,121.01119995117188,191.29220008850098]
tiempo_ldpollard=[0.003000020980834961,0.0060002803802490234,0.013000011444091797,0.015600204467773438,0.031200170516967773,0.031200170516967773,0.062400102615356445,0.09360027313232422,0.2964000701904297,0.3119997978210449]
xld_pp = [1,2,3,4,5,6,7,8,9,10]
xld_f= [1,2,3,4,5,6,7,8]

lista5 = [46191, 88369, 49651, 48159, 20609]
lista6 = [846979, 599721, 721071, 950975, 346295]
lista7 = [3239807, 2668751, 4868331, 6064247, 7183551]
lista8 = [46447573, 97961455, 61520637, 63582589, 37953139]
lista9 = [957589949, 285993255, 200223675, 993727427, 154075407]
lista10 = [3945148065, 2077524455, 1410741741, 3013455917, 7712733825]
lista15 = [913317468542225, 748978625210683, 211935444719693, 390393118631019, 575899868400667]
lista20 = [51604320814203832237, 63298031496990993641, 93152113314002488709, 82094134748542079777, 42668303529324435681]
lista25 = [9235944706891845614784115, 3717464217041394969007605, 8570068464568860651987925, 2875379783725332151103491, 9535767070476344606042013]
lista26 = [67946887789552051008439179, 52870480499543573439932129, 76401231869574802717687385, 33050631574857405494688379, 77557002475731275722629483]
lista27 = [780925575522853475955352419, 720014389960807569149531533, 720008106673540279485551917, 446089799192693571054161049, 186928968367636441424924251]
lista30 = [836577948117758985722942613799, 854202510403040818810399554939, 935666137359668426043087828925, 202441064247149515404577274991, 960379780468439013154173986349]
lista35 = [76645241700803651401124587201748681, 12823223713583358308531119681711701, 98649954850333860654599850352269507, 52064694366521480826455507641371515, 99286329004398911540709324694099265]
lista40 = [7668420727544971518053436518488432628883, 8032464906103930651088807409601003116383, 9948310486517235012574805696573476274511, 8348154590220022171566106027323561733821, 4154812008470255664651771153867816888691]
lista41 = [52945507683292623486061677123065756205811, 35867387490571667706708832276367254216783, 29584226128131055569826893518118147102095, 57660277373132994110845479054964640012961, 51191649068467813406622685048673895096785]



lista5_primos = [1577, 4757, 4559, 3071, 1007]
lista6_primos = [87847, 87271, 316159, 19511, 188561]
lista7_primos = [359893, 489347, 19879, 88163, 509017]
lista8_primos = [8241241, 29590747, 60880739, 35470933, 31341451]
lista9_primos = [34384457, 21894469, 8318159, 10381381, 52533491]
lista10_primos = [5826457841, 1791424123, 8435622953, 2990599379, 698162891]
lista15_primos = [70729893669023, 79693862188417, 11119413525721, 37723912694123, 27222054586633]
lista16_primos = [2437234439168057, 3042873855569269, 2767308355374817, 789388658097239, 3485262136807699]
lista17_primos = [1886483326161011, 3814565220378889, 1313344016610407, 1244666177261887, 691426382952667]
lista18_primos = [352766491475788123, 93092634670554269, 196725978814844483, 287774776865532487, 258537801291016081]
lista19_primos = [182715041704738129, 198473520017225017, 216695111769168709, 361931231982748801, 196025261991947279]
lista20_primos = [23832700531121320493, 32067152828622175193, 64838294355389912957, 77731138202499790837, 33423477292403677723]
lista21_primos = [53600866259326776197, 22793570657777597263, 18074032185982204823, 33930605840215624663, 13601238120718019917]
lista22_primos = [1672199105076190147777, 2909110242661320153353, 4328742703764961215059, 3818893662431602043423, 806167066427286906967]
lista23_primos = [1837234651222510016357, 773156809788269489413, 1180323349661192958047, 5001869053883149133767, 2179275228669485638001]
lista25_primos = [468005510558668309872259, 544238069390407160922089, 202666659583753040985703, 249812478106396177087649, 530320315648038911308949]
lista30_primos = [349918146876821449306418779589, 206602364307104253637740363733, 613006584758208824755166300473, 948179851363658864249921518783, 286495981162490897726704631897]

#Los tiempos fuerza bruta no funcionan con numeros productos de primos de 28 cifras!
tiempos_fb = [0.0002723217010498047, 0.00034456253051757814, 0.0003478527069091797, 0.00044956207275390623, 0.0005135059356689454, 0.0009255886077880859, 0.016902446746826172, 0.02760634422302246, 1.339552402496338, 2.5072630405426026,4.927287149429321]

#Los tiempos fuerza bruta no funcionan con numeros productos de primos de 20 cifras!
tiempos_fb_primos = [0.00019092559814453124, 0.0002642631530761719, 0.0002818107604980469, 0.0009270191192626953, 0.0008560657501220703, 0.003333568572998047, 0.25221872329711914, 1.613796329498291, 1.1491723537445069, 14.669361448287964, 16.867420434951782]

# Los tiempos fermat no funcionan con numeros de 10 cifras!
tiempos_fermat = [0.002565908432006836, 0.04211225509643555, 0.00943770408630371, 0.028308868408203125, 4.088871574401855, 99.91973805427551]

# 20 cifras
tiempos_fermat_primos = [0.0003816127777099609, 0.0009403228759765625, 0.0007202625274658203, 0.0013695716857910155, 0.0013250350952148438, 0.004761886596679687, 0.7187267303466797, 888.2101609230042]

# Los tiempos de pollard no funcionan con numeros de 42 cifras
tiempos_pollard = [0.0004434108734130859, 0.0004404544830322266, 0.0006488800048828125, 0.0007706165313720703, 0.0008330821990966796, 0.0011154651641845704, 0.0022962093353271484, 0.005032730102539062, 0.0080963134765625, 0.026056623458862303, 0.03912820816040039, 1.6526556015014648, 40.911604976654054]

# 28 cifras
tiempos_pollard_primos = [0.00038447380065917967, 0.0005166053771972657, 0.0005702972412109375, 0.0008878707885742188, 0.00022954940795898436, 0.0015295982360839845, 0.006908845901489258, 0.2487804889678955, 0.20681509971618653, 0.8142501831054687, 0.8326740741729737, 2.2809261322021483]


xfb = [5,6,7,8,9,10,15,20,25,26,27]
xfb_primos = [5,6,7,8,9,10,15,16,17,18,19]
xfermat = [5,6,7,8,9,10]
xfermat_primos = [5,6,7,8,9,10,15,20]
xpollard = [5,6,7,8,9,10,15,20,25,30,35,40,41]
xpollard_primos = [5,6,7,8,9,10,15,20,25,26,27,28]

"""
trx.figure(num=1)
trx.xlabel("Cifras")
trx.ylabel("Tiempo (s)")
trx.ylim(0,5)
trx.plot(xfb,tiempos_fb)
trx.legend(loc="lower right")
trx.title('Analisis de los tiempos de Fuerza Bruta con numeros al azar')
trx.show()


trx.figure(num=2)
trx.xlabel("Cifras")
trx.ylabel("Tiempo (s)")
trx.ylim(0,20)
trx.xlim(0,18)
trx.plot(xfb_primos,tiempos_fb_primos)
trx.legend(loc="lower right")
trx.title('Analisis de los tiempos de Fuerza Bruta con numeros productos de primos')
trx.show()


trx.figure(num=3)
trx.xlabel("Cifras")
trx.ylabel("Tiempo (s)")
trx.ylim(0,100)
trx.plot(xfermat,tiempos_fermat)
trx.legend(loc="lower right")
trx.title('Analisis de los tiempos de Fermat con numeros al azar')
trx.show()


trx.figure(num=4)
trx.xlabel("Cifras")
trx.ylabel("Tiempo (s)")
trx.ylim(0,20)
trx.plot(xfermat_primos,tiempos_fermat_primos)
trx.legend(loc="lower right")
trx.title('Analisis de los tiempos de Fermat con numeros productos de primos')
trx.show()


trx.figure(num=5)
trx.xlabel("Cifras")
trx.ylabel("Tiempo (s)")
trx.ylim(0,40)
trx.plot(xpollard,tiempos_pollard)
trx.legend(loc="lower right")
trx.title('Analisis de los tiempos de Pollard con numeros al azar')
trx.show()

trx.figure(num=6)
trx.xlabel("Cifras")
trx.ylabel("Tiempo (s)")
trx.ylim(0,2.29)
trx.xlim(0,29)
trx.plot(xpollard_primos,tiempos_pollard_primos)
trx.legend(loc="lower right")
trx.title('Analisis de los tiempos de Pollard con numeros productos de primos')
trx.show()

    trx.figure(num=9)
    trx.xlabel("Cifras")
    trx.ylabel("Tiempo (s)")
    trx.ylim(0,0.5)
    trx.plot(xld_pp,tiempo_ldpollard)
    trx.legend(loc="lower right")
    trx.title('Análisis de tiempo para la solución de Logaritmo Discreto con Pollard ')
    trx.show()

    trx.figure(num=8)
    trx.xlabel("Cifras")
    trx.ylabel("Tiempo (s)")
    trx.ylim(0,1)
    trx.plot(xld_pp,tiempo_ldpaso)
    trx.legend(loc="lower right")
    trx.title('Análisis de tiempo para la solución de Logaritmo Discreto con Paso Enano ')
    trx.show()

    trx.figure(num=7)
    trx.xlabel("Cifras")
    trx.ylabel("Tiempo (s)")
    trx.ylim(0,100)
    trx.plot(xld_f,tiempo_ldfuerza)
    trx.legend(loc="lower right")
    trx.title('Análisis de tiempo para la solución de Logaritmo Discreto con Fuerza Bruta ')
    trx.show()
"""
