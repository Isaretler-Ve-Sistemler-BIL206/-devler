import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# İşaretin özellikleri
duration = 3 # 3 saniyelik bir işaret
sampling_freq = 44100 # Ses örnekleme frekansı (Hz)

# İşaretin zaman vektörünü oluşturma
time_vector = np.arange(0, duration, 1/sampling_freq)

# Sinirsel işaretini oluşturma
signal = signal.square(2 * np.pi * 10 * time_vector)

# İşareti çizme
plt.plot(time_vector, signal)
plt.xlabel('Zaman (saniye)')
plt.ylabel('Genlik')
plt.title('Sinirsel İşaret')
plt.show()