import numpy as np
import matplotlib.pyplot as plt

# İşaretin özellikleri
freq = 2 # Frekansı 2 Hz olan bir sinüs işareti
duration = 3 # 3 saniyelik bir işaret
sampling_freq = 44100 # Ses örnekleme frekansı (Hz)

# İşaretin zaman vektörünü oluşturma
time_vector = np.arange(0, duration, 1/sampling_freq)

# Sinüs işaretini oluşturma
signal = np.sin(2 * np.pi * freq * time_vector)

# Kare dalga formuna dönüştürme
signal[signal>=0] = 1
signal[signal<0] = -1

# İşareti çizme
plt.plot(time_vector, signal)
plt.xlabel('Zaman (saniye)')
plt.ylabel('Genlik')
plt.title('Kare Dalga')
plt.show()