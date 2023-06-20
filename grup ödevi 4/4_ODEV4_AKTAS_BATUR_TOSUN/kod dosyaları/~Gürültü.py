import numpy as np
import matplotlib.pyplot as plt

# İşaretin özellikleri
duration = 3 # 3 saniyelik bir işaret
sampling_freq = 44100 # Ses örnekleme frekansı (Hz)

# İşaretin zaman vektörünü oluşturma
time_vector = np.arange(0, duration, 1/sampling_freq)

# Gürültü işaretini oluşturma
signal = np.random.uniform(low=-1, high=1, size=len(time_vector))

# İşareti çizme
plt.plot(time_vector, signal)
plt.xlabel('Zaman (saniye)')
plt.ylabel('Genlik')
plt.title('Gürültü')
plt.show()