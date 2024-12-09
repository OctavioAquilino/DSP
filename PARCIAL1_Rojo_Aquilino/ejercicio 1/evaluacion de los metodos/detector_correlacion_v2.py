import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate
import matplotlib.pyplot as plt

fs, data = wavfile.read('martin_m1.wav')
t = np.arange(len(data)) / fs

kernel_1200Hz = np.sin(2 * np.pi * 1200 * t)
kernel_1200Hz /= np.linalg.norm(kernel_1200Hz)

correlacion = correlate(data, kernel_1200Hz, mode='same')

duracion_segundos = 10
inicio = int(len(correlacion) * 3 / 4 - duracion_segundos * fs)
fin = int(len(correlacion) * 3 / 4 + duracion_segundos * fs)

tiempo = np.arange(inicio, fin) / fs

plt.figure(figsize=(10, 5))
plt.plot(tiempo, correlacion[inicio:fin])
plt.title('Porción de Correlación con Tono de 1200 Hz (10s por lado)')
plt.xlabel('Tiempo (segundos)')
plt.ylabel('Amplitud')
plt.grid()
plt.show()
