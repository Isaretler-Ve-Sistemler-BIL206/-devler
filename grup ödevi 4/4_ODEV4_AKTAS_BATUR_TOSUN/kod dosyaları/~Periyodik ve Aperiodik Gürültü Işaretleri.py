import numpy as np
import matplotlib.pyplot as plt

def periodic_noise(duration, sampling_rate, frequency, amplitude):
    time = np.arange(0, duration, 1 / sampling_rate)
    s = amplitude * np.sin(2 * np.pi * frequency * time)
    return time, s

def aperiodic_noise(duration, sampling_rate, amplitude):
    time = np.arange(0, duration, 1 / sampling_rate)
    s = amplitude * np.random.randn(len(time))
    return time, s

# Örnek kullanım
time, signal = periodic_noise(duration=1, sampling_rate=44100, frequency=1000, amplitude=0.5)
plt.plot(time, signal)
plt.show()

time, signal = aperiodic_noise(duration=1, sampling_rate=44100, amplitude=0.5)
plt.plot(time, signal)
plt.show()
