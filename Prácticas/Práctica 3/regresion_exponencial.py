# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 21:37:21 2020

@author: carlo
"""

import numpy as np

# Los tiempos fuerza bruta no funcionan con numeros productos de primos de 28 cifras!
tiempos_fb = [0.016902446746826172, 0.02760634422302246,
              1.339552402496338, 2.5072630405426026, 4.927287149429321, 63.68463110923767]
fb_cif_ini = 11
aumento_fb = 8.335606961167008
estim_fb = 1.394766457605177e+34 # Estimación con 50 cifras

# Los tiempos fuerza bruta no funcionan con numeros productos de primos de 20 cifras!
tiempos_fb_primos = [0.0031428813934326174, 1.5499239921569825, 1.5408389568328857,
                     1.1006623268127442, 14.39437837600708, 16.40034899711609, 206.0794906616211]
fb_primos_cif_ini = 6
aumento_fb_primos = 76.27775055615254
estim_fb_primos = 2.1029773066486474e+80

# Los tiempos fermat no funcionan con numeros de 10 cifras!
tiempos_fermat = [0.002565908432006836, 0.04211225509643555, 0.00943770408630371, 0.028308868408203125,
                  4.088871574401855, 99.91973805427551]
fermat_cif_ini = 5
aumento_fermat = 37.70214138066807
estim_fermat = 2.2167256626584056e+68

# 18 cifras
tiempos_fermat_primos = [0.002306509017944336, 0.0023901939392089845,
                         0.00247807502746582, 0.010994815826416015, 5.942388963699341, 8.430172872543334,
                         14.532694435119629, 129.06682448387147]
fermat_primos_cif_ini = 7
aumento_fermat_primos = 62.686213496641436
estim_fermat_primos = 4.378776394397684e+74

# Los tiempos de pollard no funcionan con numeros de 42 cifras
tiempos_pollard = [0.0011154651641845704, 0.0022962093353271484, 0.005032730102539062,
                   0.0080963134765625, 0.026056623458862303, 0.03912820816040039, 1.6526556015014648,
                   40.911604976654054]
pollard_cif_ini = 10
aumento_pollard = 6.970431406246642
estim_pollard = 5.995733542705329e+30

# 30 cifras
tiempos_pollard_primos = [0.0011094093322753906, 0.001357698440551758, 0.018590736389160156, 0.2539022922515869,
                          0.5273216724395752, 0.5921258449554443, 0.8036890983581543, 7.991343784332275,
                          9.842744874954224, 26.54191737174988, 38.85830988883972, 98.68661375045777]
pollard_primos_cif_ini = 9
aumento_pollard_primos = 3.726188474557196
estim_pollard_primos = 2.9305515186779655e+20

# -----------------------------------------------------------------------------

def regresion_exponencial(lista_tiempos):
    l_t = np.array(lista_tiempos)
    aumentos_tiempos = l_t[1:] / l_t[:-1]
    media_aumentos = np.average(aumentos_tiempos)
    
    return media_aumentos

def estimacion_tiempo_exponencial(cifras_iniciales, cifras_finales, tiempo_inicial, media_aumento_tiempos):
    num_aumentos = cifras_finales-cifras_iniciales
    
    return tiempo_inicial*media_aumento_tiempos**num_aumentos