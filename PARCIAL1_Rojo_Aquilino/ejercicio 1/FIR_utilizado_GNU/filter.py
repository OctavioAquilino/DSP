import numpy as np
from scipy.signal import firwin, freqz
import matplotlib.pyplot as plt

fs = 22050  
fcd = 1100 
fcu = 1300
num_taps = 121  

fir_filter = firwin(num_taps, cutoff=[fcd,fcu], fs=fs,pass_zero=False)
print(fir_filter)

with open("fir_taps_1200hz.txt", "w") as f:
    f.write(','.join(map(str, fir_filter)))

w, h = freqz(fir_filter, fs=fs)
plt.plot(w, 20 * np.log10(abs(h)))
plt.title('Respuesta en frecuencia del filtro FIR ')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud (dB)')
plt.grid()
plt.show()