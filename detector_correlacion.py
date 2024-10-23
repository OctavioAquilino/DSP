import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate
import matplotlib.pyplot as plt

# Cargar el archivo WAV
fs, data = wavfile.read('martin_m1.wav')

# Crear un tono de 1200 Hz
t = np.arange(len(data)) / fs
kernel_1200Hz = np.sin(2 * np.pi * 1200 * t)

# Calcular la correlación cruzada
correlacion = correlate(data, kernel_1200Hz, mode='same')

# Visualizar la correlación
plt.plot(correlacion)
plt.title('Correlación con Tono de 1200 Hz')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.show()
