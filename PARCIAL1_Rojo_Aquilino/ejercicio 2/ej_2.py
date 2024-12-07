from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import numpy as np

ruta_archivo = './martin_m1.wav'
fs, señal_wav = wavfile.read(ruta_archivo)
if fs != 22050:
    raise ValueError("La frecuencia de muestreo debe ser 22050 Hz.")
if señal_wav.ndim > 1:
    señal_wav = señal_wav[:, 0] 

# 3. Parámetros para el filtro FIR
n_taps = 121 
lowcut = 1500  # Frecuencia inferior (Hz)
highcut = 2300  # Frecuencia superior (Hz)

# 4. Diseño del filtro FIR pasa banda
filtro_fir = firwin(n_taps, [lowcut, highcut], pass_zero='bandpass', fs=fs)

# 5. Guardar los coeficientes del filtro FIR en un archivo .txt
ruta_taps = './taps_fir_martin.txt'
taps_str = ', '.join(map(str, filtro_fir))

with open(ruta_taps, 'w') as file:
    file.write(taps_str)

señal_filtrada = lfilter(filtro_fir, 1.0, señal_wav)

señal_filtrada_centrada = señal_filtrada - np.mean(señal_filtrada)

# 8. Normalizar la señal filtrada centrada a un rango de 0 a 1V
señal_tension = (señal_filtrada_centrada - np.min(señal_filtrada_centrada)) / (np.max(señal_filtrada_centrada) - np.min(señal_filtrada_centrada))

# 9. Guardar la señal resultante en un nuevo archivo .wav
ruta_salida = './salida_filtrada_martin.wav' 
señal_tension_int = np.int16(señal_tension * 32767)  
wavfile.write(ruta_salida, fs, señal_tension_int)

print("El archivo filtrado se ha guardado como:", ruta_salida)
