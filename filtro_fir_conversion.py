from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import matplotlib.pyplot as plt

# Cargar el archivo WAV
fs, data = wavfile.read('martin_m1.wav')

# Diseño del filtro pasa-bajas para eliminar 1500-2300 Hz
num_taps = 101
fir_coef = firwin(num_taps, [1500, 2300], pass_zero='bandstop', fs=fs)

# Filtrar la señal
señal_filtrada = lfilter(fir_coef, 1, data)

# Visualizar la señal de tensión filtrada
plt.plot(señal_filtrada)
plt.title('Conversión de Frecuencia a Tensión')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.show()
