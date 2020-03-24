# -*- coding: utf-8 -*-

import math

# Calcula la raíz cuadrada de un número bien calculada, usada el método
# de Newton Raphson
def raiz(n):
    i = 0
    m = (len(bin(n))-1) // 2
    x = 1 << m
    y = (x**2+n)//(2*x)
    while x > y:
        (x,y) = (y,(y**2+n)//(2*y))
        i+=1
    return [x,i] # i -> número de iteraciones necesarias para calcular sqrt(n)


a = 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890

print('%F' % math.sqrt(a*a+a))
print(raiz(a*a+a))

