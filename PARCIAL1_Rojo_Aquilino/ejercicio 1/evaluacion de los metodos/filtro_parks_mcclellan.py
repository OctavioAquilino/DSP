from scipy.io import wavfile
from scipy.signal import remez, lfilter
import matplotlib.pyplot as plt

fs, data = wavfile.read('martin_m1.wav')

num_taps = 101
bandas = [0, 1000, 1100, 1300, 1400, fs/2]
respuesta = [0, 1, 0]

fir_coef = remez(num_taps, bandas, respuesta, fs=fs)

señal_filtrada = lfilter(fir_coef, 1, data)

plt.plot(señal_filtrada)
plt.title('Señal Filtrada con Parks/McClellan')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.show()
