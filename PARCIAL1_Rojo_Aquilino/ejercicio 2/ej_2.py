from scipy.io import wavfile
from scipy.signal import firwin, lfilter, freqz
import numpy as np
import matplotlib.pyplot as plt

ruta_archivo = './martin_m1.wav'
fs, señal_wav = wavfile.read(ruta_archivo)
if fs != 22050:
    raise ValueError("La frecuencia de muestreo debe ser 22050 Hz.")
if señal_wav.ndim > 1:
    señal_wav = señal_wav[:, 0] 

n_taps = 121 
lowcut = 1500  
highcut = 2300  

filtro_fir = firwin(n_taps, [lowcut, highcut], pass_zero='bandpass', fs=fs)

ruta_taps = './taps_fir_martin_test.txt'
taps_str = ', '.join(map(str, filtro_fir))

with open(ruta_taps, 'w') as file:
    file.write(taps_str)

señal_filtrada = lfilter(filtro_fir, 1.0, señal_wav)

señal_filtrada_centrada = señal_filtrada - np.mean(señal_filtrada)

señal_tension = (señal_filtrada_centrada - np.min(señal_filtrada_centrada)) / (np.max(señal_filtrada_centrada) - np.min(señal_filtrada_centrada))

ruta_salida = './salida_filtrada_martin.wav' 
señal_tension_int = np.int16(señal_tension * 32767)  
wavfile.write(ruta_salida, fs, señal_tension_int)

print("El archivo filtrado se ha guardado como:", ruta_salida)

frecuencia, respuesta = freqz(filtro_fir, worN=8000, fs=fs)
plt.figure(figsize=(10, 6))
plt.plot(frecuencia, 20 * np.log10(abs(respuesta)), label="Respuesta del filtro")
plt.title("Respuesta en frecuencia del filtro FIR")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud (dB)")
plt.grid()
plt.axvline(lowcut, color='red', linestyle='--', label=f"Corte inferior: {lowcut} Hz")
plt.axvline(highcut, color='green', linestyle='--', label=f"Corte superior: {highcut} Hz")
plt.legend()
plt.show()