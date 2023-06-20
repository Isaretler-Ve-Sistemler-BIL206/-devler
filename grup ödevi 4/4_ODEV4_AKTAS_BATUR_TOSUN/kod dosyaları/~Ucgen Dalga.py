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

# Üçgen dalga formuna dönüştürme
signal = np.abs(signal)
signal = 2 * (signal / np.max(signal)) - 1

# İşareti çizme
plt.plot(time_vector, signal)
plt.xlabel('Zaman (saniye)')
plt.ylabel('Genlik')
plt.title('Üçgen Dalga')
plt.show()