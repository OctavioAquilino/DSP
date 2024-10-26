from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import numpy as np
import matplotlib.pyplot as plt

# 1. Leer el archivo .wav proporcionado
ruta_archivo = 'C:/Users/tayia/Desktop/DSP/martin_m1.wav'  # Cambiar por la ruta correcta
fs, señal_wav = wavfile.read(ruta_archivo)

# 2. Confirmar que la frecuencia de muestreo sea 22050 Hz y que la señal sea mono
if fs != 22050:
    raise ValueError("La frecuencia de muestreo debe ser 22050 Hz.")
if señal_wav.ndim > 1:
    señal_wav = señal_wav[:, 0]  # Tomar solo el primer canal si es estéreo

# 3. Parámetros para el filtro FIR
n_taps = 101  # Número de coeficientes del filtro, ajustable según la precisión deseada
lowcut = 1500  # Frecuencia inferior (Hz)
highcut = 2300  # Frecuencia superior (Hz)

# 4. Diseño del filtro FIR pasa banda
filtro_fir = firwin(n_taps, [lowcut, highcut], pass_zero='bandpass', fs=fs)

# 5. Aplicar el filtro FIR a la señal .wav
señal_filtrada = lfilter(filtro_fir, 1.0, señal_wav)

# 6. Centrar la señal en 0V
#señal_filtrada = señal_filtrada - np.mean(señal_filtrada)

# 7. Normalizar la señal a un rango de 0 a 1V
señal_tension = (señal_filtrada - np.min(señal_filtrada)) / (np.max(señal_filtrada) - np.min(señal_filtrada))

# 8. Visualizar la señal normalizada en el dominio del tiempo
plt.figure(figsize=(10, 4))
plt.plot(señal_tension[800:1800])  # Muestra una parte de la señal para mayor claridad
plt.title('Señal Normalizada en el Dominio del Tiempo')
plt.xlabel('Muestras')
plt.ylabel('Amplitud (0 a 1V)')
plt.grid(True)
plt.show()
