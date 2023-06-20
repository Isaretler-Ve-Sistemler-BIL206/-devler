import wave
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Ses dosyası adı ve analiz parametreleri
FILENAME = "TestSesKaydı.wav"
OUTPUT_FILENAME = "output.wav"
WINDOW_SIZE = 30 # 30ms bölümler halinde analiz edilecek
ENERGY_THRESHOLD = 8000 # Gürültüyü belirlemek için kullanılan enerji eşik değeri
ZCR_THRESHOLD = 0.005 # Duraksamaları belirlemek için kullanılan sıfır-geçiş sayısı eşik değeri

# Ses dosyasını aç
with wave.open(FILENAME, 'rb') as wf:
    # Ses parametrelerini oku
    sample_width = wf.getsampwidth()
    sample_rate = wf.getframerate()
    num_channels = wf.getnchannels()
    num_frames = wf.getnframes()

    # Yeni dosya için Wave_write nesnesi oluştur
    output_wf = wave.open(OUTPUT_FILENAME, 'wb')
    output_wf.setnchannels(num_channels)
    output_wf.setsampwidth(sample_width)
    output_wf.setframerate(sample_rate)

    # PyAudio stream oluştur
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=num_channels,
                    rate=sample_rate,
                    output=True)

    # Matplotlib grafik penceresini oluştur
    fig, ax = plt.subplots(3, 1,  figsize=(14, 7))
    fig.tight_layout(h_pad=3)
    # Grafiklerin yerleşimini ve boyutunu ayarla
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.95)

    # ses kaydı grafiği
    ax[0].set_ylim([-2**15, 2**15]) # Y ekseni sınırlarını ayarla
    ax[0].set_xlim([0, num_frames / sample_rate]) # X ekseni sınırlarını ayarla
    ax[0].set_xlabel("Zaman (s)")
    ax[0].set_ylabel("Ses Şiddeti")

    # enerji grafiği
    ax[1].set_ylim([-2**15, 2**15]) # Y ekseni sınırlarını ayarla
    ax[1].set_xlim([0, num_frames / sample_rate]) # X ekseni sınırlarını ayarla
    ax[1].set_xlabel("Zaman (s)")
    ax[1].set_ylabel("enerji")

    # sıfır-geçiş sayısı grafiği
    ax[2].set_ylim([-2**15, 2**15]) # Y ekseni sınırlarını ayarla
    ax[2].set_xlim([0, num_frames / sample_rate]) # X ekseni sınırlarını ayarla
    ax[2].set_xlabel("Zaman (s)")
    ax[2].set_ylabel("zsc")

    energies = []
    zcrs = []

    # Ses dosyasındaki her bölüm için
    window_size = int(sample_rate * WINDOW_SIZE / 1000) # Milisaniye cinsinden bölüm boyutu

    temp = 0

    for i in range(0, num_frames, window_size):
        # Bölümü oku
        wf.setpos(i)
        data = wf.readframes(window_size)

        # Bölümü numpy dizisine dönüştür
        signal = np.array(struct.unpack('{}h'.format(len(data) // sample_width), data))

        # Enerji hesapla
        energy = np.sum(signal ** 2) / len(signal)
        energies.append(energy)

        # Sıfır-geçiş sayısını hesapla
        zcr = np.sum(np.abs(np.diff(np.sign(signal)))) / (2 * len(signal))
        zcrs.append(zcr)

        # Bölümü belirleyin: konuşma veya gürültü/duraksama
        if energy >= ENERGY_THRESHOLD and zcr >= ZCR_THRESHOLD:
            label = "konuşma"

            # Konuşma bölümünü kaydet
            # stream.write(data)

            # konuşma bçlümünü yeni ses dosyasına yaz
            output_wf.writeframes(data)
            
            # temp değişkeni, ses bölümleri arasındaki dalgalanmayı azaltmak için kullandık. konuşma olarak algılnan bir bölümün hemen sonrasındaki bölümü sessizlik olsa bile konuşma olarak # kaydediyoruz. oynatma hıznı normalleştirmek için bunu ekledik.
            temp = 1
           
        else:
            if temp > 0:
                label = "konuşma"
                # Konuşma bölümünü kaydet
                # stream.write(data)

                # konuşma bçlümünü yeni ses dosyasına yaz
                output_wf.writeframes(data)
                temp -= 1
            else:
                label = "gürültü/duraksama"

        # Grafikte bölümü çiz
        time = i / sample_rate
        ax[0].plot([time, time + WINDOW_SIZE/1000], [np.min(signal), np.max(signal)], color="red" if label == "konuşma" else "gray")

    # Enerji grafiğini çiz
    ax[1].set_ylim([0, np.max(energies) * 1.1])
    time_points = np.linspace(0, num_frames / sample_rate, len(energies))
    ax[1].plot(time_points, energies, color='blue')

    # ZCR grafiğini çiz
    ax[2].set_ylim([0, np.max(zcrs) * 1.1])
    ax[2].plot(time_points, zcrs, color='green')

    # Yeni dosyayı kapat
    output_wf.close()

    # Streami kapat
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Çalma butonunu oluştur
    play_button_ax = plt.axes([0.90, 0.91, 0.1, 0.04])
    play_button = Button(play_button_ax, 'yeni kaydı oynat', color='lightblue', hovercolor='skyblue')

    # Çalma butonunu oluştur
    play_button2_ax = plt.axes([0.90, 0.85, 0.1, 0.04])
    play_button2 = Button(play_button2_ax, 'eski kaydı oynat', color='lightblue', hovercolor='skyblue')

    # Ses kaydını oynatan fonksiyon
    def play_recorded_audio(event, filename):
        # Yeni dosyayı aç
        with wave.open(filename, 'rb') as recorded_wf:
        # PyAudio stream oluştur
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(sample_width),
                            channels=num_channels,
                            rate=sample_rate,
                            output=True)

            # Kaydedilen ses dosyasını oku
            data = recorded_wf.readframes(num_frames)

            # Ses dosyasını çal
            stream.write(data)

            # Streami kapat
            stream.stop_stream()
            stream.close()
            p.terminate()

    # Oynat butonuna tıklama işlevini ekle
    play_button.on_clicked(lambda event: play_recorded_audio(event, OUTPUT_FILENAME))
    play_button2.on_clicked(lambda event: play_recorded_audio(event, FILENAME))


    # Grafik penceresini göster
    plt.show()