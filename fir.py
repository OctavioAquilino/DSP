from scipy.signal import firwin
import numpy as np

# Parámetros del filtro
num_taps = 101  # Número de coeficientes (ajústalo según tus necesidades)
fs = 48000  # Frecuencia de muestreo (ajústala según tus datos)
cutoff_freq = [1500, 2300]  # Frecuencias de corte (en Hz) para un filtro pasa-bandas

# Diseño del filtro FIR pasa-bandas
fir_coef = firwin(num_taps, cutoff_freq, pass_zero='bandstop', fs=fs)

# Guardar los coeficientes en un archivo de texto
np.savetxt('fir_taps.txt', fir_coef, fmt='%.18e')

print(fir_coef)
