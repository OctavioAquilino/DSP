import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def goertzel(s, fs, target_freq):
    """Implementación del algoritmo de Goertzel para detectar una frecuencia específica."""
    n = len(s)
    k = int(0.5 + (n * target_freq / fs))
    w = 2 * np.pi * k / n
    cos_w = np.cos(w)
    coef = 2 * cos_w

    s_prev = 0
    s_prev2 = 0

    for sample in s:
        s_next = sample + coef * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s_next

    # Cálculo de la potencia en la frecuencia objetivo
    power = s_prev2**2 + s_prev**2 - coef * s_prev * s_prev2
    return power

# Cargar el archivo WAV
fs, data = wavfile.read('martin_m1.wav')

# Aplicar el algoritmo de Goertzel para detectar 1200 Hz
target_freq = 1200
power = goertzel(data, fs, target_freq)

print(f"Potencia detectada en {target_freq} Hz: {power}")
