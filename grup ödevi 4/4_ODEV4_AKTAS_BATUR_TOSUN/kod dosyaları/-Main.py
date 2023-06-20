import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Subplotları oluşturma ve sinyalleri grafiğe çizme
# 4 satır ve 2 sütuna sahip bir dizi oluşturuldu (array), ilk açılan ekranın boyutu 12,10 olarak ayarlandı
fig, axs = plt.subplots(4, 2, figsize=(12, 10))
# bu satır sayesinde nesneler arasında mesafe oluşturuldu
fig.tight_layout(h_pad=5)
# görsel düzenleme için konulmuş bir satırdır nesneleri biraz kaydırır
plt.subplots_adjust(top=0.95)

def gurultuIsaretiCiz(axs):
    # İşaretin özellikleri
    duration = 0.05 # 0.05 saniyelik bir işaret
    sampling_freq = 44100 # Ses örnekleme frekansı (Hz)

    # İşaretin zaman vektörünü oluşturma
    time_vector = np.arange(0, duration, 1/sampling_freq)

    # Gürültü işaretini oluşturma
    signal = np.random.uniform(low=-1, high=1, size=len(time_vector))

    # İşareti çizme
    axs.plot(time_vector, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Gürültü')

def kareDalgaCiz(axs):
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
    axs.plot(time_vector, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Kare Dalga')

def ucgenDalgaCiz(axs):
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
    axs.plot(time_vector, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Üçgen Dalga')

def sinirselIsaretCiz(axs):
    # İşaretin özellikleri
    duration = 3 # 3 saniyelik bir işaret
    sampling_freq = 44100 # Ses örnekleme frekansı (Hz)

    # İşaretin zaman vektörünü oluşturma
    time_vector = np.arange(0, duration, 1/sampling_freq)
    from scipy import signal
    # Sinirsel işaretini oluşturma
    signal = signal.square(2 * np.pi * 10 * time_vector)

    # İşareti çizme
    axs.plot(time_vector, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Sinirsel İşaret')

def sinusIsaretiCiz(axs):
    # İşaretin özellikleri
    freq = 2 # Frekansı 2 Hz olan bir sinüs işareti
    duration = 3 # 3 saniyelik bir işaret
    sampling_freq = 44100 # Ses örnekleme frekansı (Hz)

    # İşaretin zaman vektörünü oluşturma
    time_vector = np.arange(0, duration, 1/sampling_freq)

    # Sinüs işaretini oluşturma
    signal = np.sin(2 * np.pi * freq * time_vector)

    # İşareti çizme
    axs.plot(time_vector, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Sinüs İşareti')

def sineGaussianIsaretCiz(axs):
    def sine_gaussian_signal(duration, sampling_rate, frequency, bandwidth, amplitude):
        time = np.arange(0, duration, 1 / sampling_rate)
        t_center = duration / 2
        s = amplitude * np.exp(-(time - t_center) ** 2 / (2 * bandwidth ** 2)) * np.sin(2 * np.pi * frequency * (time - t_center))
        return time, s

    time, signal = sine_gaussian_signal(duration=1, sampling_rate=44100, frequency=1000, bandwidth=0.1, amplitude=1)
    axs.plot(time, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Sine Gaussian işaret')

def periyodikIsaretCiz(axs) :
    def periodic_noise(duration, sampling_rate, frequency, amplitude):
        time = np.arange(0, duration, 1 / sampling_rate)
        s = amplitude * np.sin(2 * np.pi * frequency * time)
        return time, s
    time, signal = periodic_noise(duration=1, sampling_rate=44100, frequency=100, amplitude=0.5)
    axs.plot(time, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Periyodik işaret')

def aPeriyodikIsaretCiz(axs) :
    def aperiodic_noise(duration, sampling_rate, amplitude):
        time = np.arange(0, duration, 1 / sampling_rate)
        s = amplitude * np.random.randn(len(time))
        return time, s

    time, signal = aperiodic_noise(duration=1, sampling_rate=44100, amplitude=0.5)
    axs.plot(time, signal)
    axs.set_xlabel('Zaman (saniye)')
    axs.set_ylabel('Genlik')
    axs.set_title('Periyodik olmayan işaret')

#1. tablo
gurultuIsaretiCiz(axs[0, 0])

#2. tablo
kareDalgaCiz(axs[1, 0])

#3. tablo
ucgenDalgaCiz(axs[2, 0])

#4. tablo
sinirselIsaretCiz(axs[3, 0])

#5. 1ablo
sinusIsaretiCiz(axs[0, 1])

# 6. tablo
sineGaussianIsaretCiz(axs[1, 1])

# 7. tablo
periyodikIsaretCiz(axs[2, 1])

# 8. tablo
aPeriyodikIsaretCiz(axs[3, 1])

plt.show()