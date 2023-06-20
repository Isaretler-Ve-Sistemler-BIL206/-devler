import numpy as np
import matplotlib.pyplot as plt

def sine_gaussian_signal(duration, sampling_rate, frequency, bandwidth, amplitude):
    time = np.arange(0, duration, 1 / sampling_rate)
    t_center = duration / 2
    s = amplitude * np.exp(-(time - t_center) ** 2 / (2 * bandwidth ** 2)) * np.sin(2 * np.pi * frequency * (time - t_center))
    return time, s

# Örnek kullanım
time, signal = sine_gaussian_signal(duration=1, sampling_rate=44100, frequency=1000, bandwidth=0.1, amplitude=1)
plt.plot(time, signal)
plt.show()