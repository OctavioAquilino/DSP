import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def goertzel(s, fs, target_freq):
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

    power = s_prev2**2 + s_prev**2 - coef * s_prev * s_prev2
    return power

fs, data = wavfile.read('martin_m1.wav')

frecuencias = np.arange(1150, 1251, 2) 

potencias = []

for freq in frecuencias:
    potencia = goertzel(data, fs, freq)
    potencias.append(potencia)

plt.plot(frecuencias, potencias)
plt.title('Potencia detectada vs Frecuencia')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Potencia')
plt.grid(True)
plt.show()
