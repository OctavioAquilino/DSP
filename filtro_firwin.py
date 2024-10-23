from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import matplotlib.pyplot as plt

# Cargar el archivo WAV
fs, data = wavfile.read('martin_m1.wav')

# Diseño del filtro FIR
num_taps = 101
fir_coef = firwin(num_taps, [1100, 1300], pass_zero='bandpass', fs=fs)

# Filtrar la señal
señal_filtrada = lfilter(fir_coef, 1, data)

# Visualizar la señal filtrada
plt.plot(señal_filtrada)
plt.title('Señal Filtrada con firwin')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.show()
