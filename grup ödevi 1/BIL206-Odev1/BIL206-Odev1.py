import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.io.wavfile import write
import pyaudio

# Öğrenci numaralarına göre düzenlenmiş frekans değerleri
fr1 = 10 * 20  # Ibrahim Serhat Aktas --- 210601020
fr2 = 20 * 9   # Kutay Can Batur -------- 210601009
fr3 = 50 * 27  # Mert Tosun ------------- 210601027


# Fonksyonlar
def play_sound(signal, framerate=44100):
    """Sinyalleri ses'e çeviren fonksyon"""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=framerate,
                    output=True)
    stream.write(signal.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def button_callback(event, signal):
    """Butona tıklandığında tetiklenecek olan fonksyon"""
    play_sound(signal)


# Sinusoidal signyali oluşturma
time = np.arange(0, 3/fr1, 1/44100)  
signal1 = 0.1 * np.sin(2*np.pi*fr1*time)
signal2 = 0.1 * np.sin(2*np.pi*fr2*time)
signal3 = 0.1 * np.sin(2*np.pi*fr3*time)
signal_sum = signal1 + signal2 + signal3


# Subplotları oluşturma ve sinyalleri grafiğe çizme
# 3 satır ve 2 sütuna sahip bir dizi oluşturuldu (array), ilk açılan ekranın boyutu 12,10 olarak ayarlandı
fig, axs = plt.subplots(3, 2, figsize=(12, 10))
# bu satır sayesinde nesneler arasında mesafe oluşturuldu
fig.tight_layout(h_pad=5)
# görsel düzenleme için konulmuş bir satırdır nesneleri biraz kaydırır
plt.subplots_adjust(top=0.95)


#1. tablo
#210601020 numarasına uygun grafiği çizer
axs[0, 0].plot(time, signal1)
axs[0, 0].set_title('Ibrahim Serhat Aktas - 210601020')
axs[0, 0].set_xlabel('Zaman (s)')
axs[0, 0].set_ylabel('Genlik')

#2. tablo
#210601009 numarasına uygun grafiği çizer
axs[1, 0].plot(time, signal2)
axs[1, 0].set_title('Kutay Can Batur - 210601009')
axs[1, 0].set_xlabel('Zaman (s)')
axs[1, 0].set_ylabel('Genlik')

#3. tablo
#210601027 numarasına uygun grafiği çizer
axs[2, 0].plot(time, signal3)
axs[2, 0].set_title('Mert Tosun - 210601027')
axs[2, 0].set_xlabel('Zaman (s)')
axs[2, 0].set_ylabel('Genlik')

#4. tablo
#Toplam sinisodel işaret grafiğini çizer
axs[0, 1].plot(time, signal_sum)
axs[0, 1].set_title('Toplam Sinusoidal İşaret')
axs[0, 1].set_xlabel('Zaman (s)')
axs[0, 1].set_ylabel('Genlik')

#5. 1ablo
#Tüm İşaretlerin Grafiğini çizer
axs[1,1].plot(time, signal1, label="210601020")
axs[1,1].plot(time, signal2, label="210601009")
axs[1,1].plot(time, signal3, label="210601027")
axs[1,1].plot(time, signal_sum, label="Toplam İşaret")
axs[1,1].set_title("Tüm İşaretlerin Grafiği")
axs[1,1].set_xlabel("Zaman (s)")
axs[1,1].set_ylabel("Genlik")
axs[1,1].legend()

# 6. tablo
# oluşturduğumuz dizi 6 elemana sahipti ama biz 5'ini kullandık
# bu yüzden 6. tablonun görünürlüğünü kapattık
axs[2,1].axis('off')

#---------------
#    Sesler 
#---------------

# Grafikleri çizerken işaretler 3 periyot uzunluğunda ayarlanmıştı
# fakat sesleri 3 periyot uzunuğunda kullandığımızda duyması çok zorlaşır
# o yüzden 3 yerine 300 periyot uzunuğunda olan yeni ses sinyalleri oluşturucaz 

sestime = np.arange(0, 300/fr1, 1/44100) 
sessignal1 = 0.1 * np.sin(2*np.pi*fr1*sestime)
sessignal2 = 0.1 * np.sin(2*np.pi*fr2*sestime)
sessignal3 = 0.1 * np.sin(2*np.pi*fr3*sestime)
sessignal_sum = sessignal1 + sessignal2 + sessignal3

# Buton ekleyerek ses çalma işlevselliği ekleme
button_ax = fig.add_axes([0.637, 0.135, 0.09, 0.05]) # buton konumu ve boyutu
play_button = Button(button_ax, 'Toplam İşaret', hovercolor='0.975') # buton oluşturma
play_button.on_clicked(lambda event: button_callback(event, sessignal_sum)) # butona tıklanınca tetiklenen olay

# Buton ekleyerek ses çalma işlevselliği ekleme
button_ax1 = fig.add_axes([0.54, 0.195, 0.09, 0.05]) # buton konumu ve boyutu
play_button1 = Button(button_ax1, '210601020', hovercolor='0.975') # buton oluşturma
play_button1.on_clicked(lambda event: button_callback(event, sessignal1)) # butona tıklanınca tetiklenen olay

# Buton ekleyerek ses çalma işlevselliği ekleme
button_ax2 = fig.add_axes([0.54, 0.135, 0.09, 0.05]) # buton konumu ve boyutu
play_button2 = Button(button_ax2, '210601009', hovercolor='0.975') # buton oluşturma
play_button2.on_clicked(lambda event: button_callback(event, sessignal2)) # butona tıklanınca tetiklenen olay

# Buton ekleyerek ses çalma işlevselliği ekleme
button_ax3 = fig.add_axes([0.54, 0.075, 0.09, 0.05]) # buton konumu ve boyutu
play_button3 = Button(button_ax3, '210601027', hovercolor='0.975') # buton oluşturma
play_button3.on_clicked(lambda event: button_callback(event, sessignal3)) # butona tıklanınca tetiklenen olay

plt.show()