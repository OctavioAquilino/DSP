from scipy.signal import firwin
import numpy as np

# Parámetros del filtro
num_taps = 101  # Número de coeficientes (ajústalo según tus necesidades)
fs = 22050  # Frecuencia de muestreo (ajústala según tus datos)
cutoff_freq = [1100, 1300]  # Frecuencias de corte (en Hz) para un filtro rechaza-bandas

# Diseño del filtro FIR rechaza-bandas
fir_coef = firwin(num_taps, cutoff_freq, pass_zero='bandstop', fs=fs)

# Convertir los coeficientes a un formato de cadena separado por comas
coef_str = ', '.join([f'{coef:.18e}' for coef in fir_coef])

# Guardar los coeficientes en un archivo de texto
with open('fir_taps.txt', 'w') as f:
    f.write(coef_str)

print(fir_coef)
