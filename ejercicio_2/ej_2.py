from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import numpy as np

# Leer el archivo .wav 
ruta_archivo = './martin_m1.wav'  
fs, señal_wav = wavfile.read(ruta_archivo)

# Confirmar la frecuencia de muestreo
if fs != 22050:
    raise ValueError("La frecuencia de muestreo debe ser 22050 Hz.")
if señal_wav.ndim > 1:
    señal_wav = señal_wav[:, 0] 

# Parámetros para el filtro FIR
n_taps = 101 
lowcut = 1500  # Frecuencia inferior (Hz)
highcut = 2300  # Frecuencia superior (Hz)

# Diseño del filtro FIR pasa banda
filtro_fir = firwin(n_taps, [lowcut, highcut], pass_zero='bandpass', fs=fs)

# Guardar los coeficientes del filtro FIR en un archivo .txt
ruta_taps = './taps_fir.txt'  
taps_str = ', '.join(map(str, filtro_fir))
with open(ruta_taps, 'w') as file:
    file.write(taps_str)

print("Los taps del filtro se han guardado como:", ruta_taps)

# Aplicar el filtro FIR a la señal
señal_filtrada = lfilter(filtro_fir, 1.0, señal_wav)

# Normalizar a un rango de 0 a 1V
señal_tension = (señal_filtrada - np.min(señal_filtrada)) / (np.max(señal_filtrada) - np.min(señal_filtrada))

# Guardar la señal resultante en un .wav
ruta_salida = './salida_filtrada.wav' 
señal_tension_int = np.int16(señal_tension * 32767)  
wavfile.write(ruta_salida, fs, señal_tension_int)

print("El archivo filtrado se ha guardado como:", ruta_salida)
