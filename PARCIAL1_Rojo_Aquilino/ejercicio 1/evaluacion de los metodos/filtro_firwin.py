from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import matplotlib.pyplot as plt

fs, data = wavfile.read('martin_m1.wav')

num_taps = 101
fir_coef = firwin(num_taps, [1100, 1300], pass_zero='bandpass', fs=fs)

señal_filtrada = lfilter(fir_coef, 1, data)

plt.plot(señal_filtrada)
plt.title('Señal Filtrada con firwin')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.show()
