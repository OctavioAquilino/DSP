from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import numpy as np

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

# 5. Guardar los coeficientes del filtro FIR en un archivo .txt
ruta_taps = 'C:/Users/tayia/Desktop/DSP/ejercicio_2/taps_fir.txt'  # Cambiar por la ruta deseada
taps_str = ', '.join(map(str, filtro_fir))
with open(ruta_taps, 'w') as file:
    file.write(taps_str)

print("Los taps del filtro se han guardado como:", ruta_taps)

# 6. Aplicar el filtro FIR a la señal .wav
señal_filtrada = lfilter(filtro_fir, 1.0, señal_wav)

# 7. Normalizar la señal filtrada a un rango de 0 a 1V
señal_tension = (señal_filtrada - np.min(señal_filtrada)) / (np.max(señal_filtrada) - np.min(señal_filtrada))

# 8. Guardar la señal resultante en un nuevo archivo .wav
ruta_salida = 'C:/Users/tayia/Desktop/DSP/ejercicio_2/salida_filtrada_sinNormalizar.wav'  # Cambiar por la ruta deseada
señal_tension_int = np.int16(señal_filtrada * 32767)  # Convertir a entero para guardar en .wav
wavfile.write(ruta_salida, fs, señal_tension_int)

print("El archivo filtrado se ha guardado como:", ruta_salida)
