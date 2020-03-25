from random import randint
from math import sqrt, floor
import time


def potenciamodular(a,b,m):
    p = 1
    while b > 0:
        if (b%2 == 1):
            p = (p*a)%m
        b = b>>1
        a = (a*a)%m
    return p

def mcd_ex(a,b):
    (u0,u1)=(1,0)
    (v0,v1)=(0,1)
    while b > 0:
        (c,r) = (a//b, a%b)
        (u0,u1) = (u1,u0-c*u1)
        (v0,v1) = (v1,v0-c*v1)
        (a,b) = (b, a%b)
    return [a,u0,v0]

def inverso(a,p):
    x = mcd_ex(a,p)
    if x[0] == 1:
        return(x[1]%p)
    print('No existe el inverso')
    return 0


def textotonumero(tex):
    sol = 0
    pos = 1
    for s in tex:
        x = ord(s)
        if (x>64 and x < 91): 
            sol = sol + pos*(x-64)
            pos*=28
        elif x == 209:
            sol = sol + pos*27
            pos*=28
        elif x == 32:
            pos*=28
    return sol

def numerototexto(num):
    texto = ''
    while num > 0:
       aux = num%28
       if aux==0:
           texto = texto + ' '
       elif aux == 27:
           texto = texto + 'Ñ'
       else:
           texto = texto + chr(aux+64)
       num = num//28
    return texto


def cifra_RSA(mensaje):
    m = textotonumero(mensaje)
    cif = potenciamodular(m,kpub[1],kpub[0])
    return(numerototexto(cif))

def descifra_RSA(mensaje_cif):
    c = textotonumero(mensaje_cif)
    m = potenciamodular(c,kpriv[1],kpriv[0])
    return(numerototexto(m))
  

# Dos primos (fuertes)
p = 12240000746791304769966673681635208178673831256350064676423691057521266822035296552090249040460261270850364872162482603267961711200272033788960905708380803
q = 10148334946549382203410554922515162413168350173331903288259172514144911161626140874638900766885636378511261520046016884287131840310798929361295078163816643

n = p*q
e = 65537
phi = (p-1)*(q-1)
d = inverso(e,phi)

kpub = (n,e)
kpriv = (n,d)
