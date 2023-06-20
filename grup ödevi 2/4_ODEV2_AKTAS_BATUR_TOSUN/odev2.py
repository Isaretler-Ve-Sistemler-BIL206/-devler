import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pyaudio
import os

# 1x2 boyutlarında bir subplot oluştur ve boyutunu ayarla.
# bunu yapmamızın sebebi grafiği ekrana düzgün bir şekilde yerleştirebilmek.
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

ax = axs[0]
ax.set_xlim([0, 9])

# x eksenindeki etiketler için kullanılacak değerleri tanımla.
# frekans değerlerini x eksenine yerleştir.
x = [0, 1, 2, 3, 4, 5, 6, 7]
x_labels = [0, 250, 500, 1000, 2000, 4000, 8000, 0] 

ax.set_xticks(x)
ax.set_xticklabels(x_labels) 

# x ve y değerlerini tanımla ve çizgi grafiği oluştur.
x = np.linspace(1, 6, 6)
y = np.array([0.05, 0.1, 2, 20, 40, 0])
line, = ax.plot(x, y, 'o-', markersize=10)

# Sinyal örneklerinin uzunluğunu belirle
uzunluk = 3000
# sinyaller için zaman aralıklarını ve sinyal örneklerini oluştur.
sestime1 = np.arange(0, uzunluk/x_labels[1], 1/44150) 
sessignal1 = y[0] * np.sin(2*np.pi*x_labels[1]*sestime1)
sestime2 = np.arange(0, uzunluk/x_labels[2], 1/44150) 
sessignal2 = y[1] * np.sin(2*np.pi*x_labels[2]*sestime2)
sestime3 = np.arange(0, uzunluk/x_labels[3], 1/44150) 
sessignal3 = y[2] * np.sin(2*np.pi*x_labels[3]*sestime3)
sestime4 = np.arange(0, uzunluk/x_labels[4], 1/44150) 
sessignal4 = y[3] * np.sin(2*np.pi*x_labels[4]*sestime4)
sestime5 = np.arange(0, uzunluk/x_labels[5], 1/44150) 
sessignal5 = y[4] * np.sin(2*np.pi*x_labels[5]*sestime5)
sestime6 = np.arange(0, uzunluk/x_labels[6], 1/44150) 
sessignal6 = y[5] * np.sin(2*np.pi*x_labels[6]*sestime6)

# bu fonksiyon grafik değiştirildikçe çağırılarak sinyallerin güncellenmesini sağlar.
def update_signal():
    global sessignal1, sessignal2, sessignal3, sessignal4, sessignal5, sessignal6
    sestime1 = np.arange(0, uzunluk/x_labels[1], 1/44150) 
    sessignal1 = y[0] * np.sin(2*np.pi*x_labels[1]*sestime1)
    sestime2 = np.arange(0, uzunluk/x_labels[2], 1/44150) 
    sessignal2 = y[1] * np.sin(2*np.pi*x_labels[2]*sestime2)
    sestime3 = np.arange(0, uzunluk/x_labels[3], 1/44150) 
    sessignal3 = y[2] * np.sin(2*np.pi*x_labels[3]*sestime3)
    sestime4 = np.arange(0, uzunluk/x_labels[4], 1/44150) 
    sessignal4 = y[3] * np.sin(2*np.pi*x_labels[4]*sestime4)
    sestime5 = np.arange(0, uzunluk/x_labels[5], 1/44150) 
    sessignal5 = y[4] * np.sin(2*np.pi*x_labels[5]*sestime5)
    sestime6 = np.arange(0, uzunluk/x_labels[6], 1/44150) 
    sessignal6 = y[5] * np.sin(2*np.pi*x_labels[6]*sestime6)

# Grafiği güncellemek için kullanacağımız fonksiyon.
def update_plot():
    line.set_ydata(y)
    fig.canvas.draw_idle()
    update_signal()
    for i, (x_val, y_val) in enumerate(zip(x, y)):
        vv = str(y_val)[:6]
        textler[i].set_text(vv)

# Fare tıklandığında çağrılacak olan fonksiyon.
def on_press(event):
    # Eğer fare grafiğin içinde değilse hiçbir şey yapmıyoruz.
    if event.inaxes != ax:
        return
    # En yakın x koordinatına sahip noktanın dizindeki index'ini buluyoruz.
    index = np.argmin(np.abs(x - event.xdata))
    # Hangi noktanın sürüklendiğini takip etmek için bir değişken kullanıyoruz.
    global currently_dragging
    currently_dragging = index

# Fare hareket ettiğinde çağrılacak olan fonksiyon.
def on_motion(event):
    # Eğer hiçbir nokta sürüklenmiyorsa hiçbir şey yapmıyoruz.
    if currently_dragging is None:
        return
    # Sürüklenen noktanın y koordinatını güncelliyoruz.
    y[currently_dragging] = event.ydata
    # Grafiği güncelliyoruz.
    update_plot()

# Fare düğmesi serbest bırakıldığında çağrılacak olan fonksiyon.
def on_release(event):
    # Hangi noktanın sürüklendiğini takip etmek için kullanılan değişkeni None olarak ayarlıyoruz.
    global currently_dragging
    currently_dragging = None

# Buton olaylarını dinleyeceğimiz bağlantıları tanımlıyoruz.
cid_press = fig.canvas.mpl_connect('button_press_event', on_press)
cid_motion = fig.canvas.mpl_connect('motion_notify_event', on_motion)
cid_release = fig.canvas.mpl_connect('button_release_event', on_release)

# Şu anda hangi noktanın sürüklendiğini takip etmek için kullanılan değişkeni None olarak ayarlıyoruz.
currently_dragging = None       

# varsayılan ayarlara dönmek için kullanılan fonksiyon.
#varsayılan ayarlar, ödev dosyasında belirlenen değerlerdir.
def reset(event):
    global y
    y = np.array([0.05, 0.1, 2, 20, 40, 0])
    update_plot()
    
ax.grid()

# ses sinyallerini çalmak için kullandığımız fonksiyon.
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

# bu fonksiyon grafikte belirlenen tüm frekansların toplamının sesini çalmak için.
def button_callback(event):
    update_signal()
    min_length = min(len(sessignal1), len(sessignal2), len(sessignal3), len(sessignal4), len(sessignal5))
    sessignal_sum = sessignal1[:min_length] + sessignal2[:min_length] + sessignal3[:min_length] + sessignal4[:min_length] + sessignal5[:min_length]
    play_sound(sessignal_sum)

# Diğer buton ve çeşitli görsel düzenlemeler

ax_button = plt.axes([0.56, 0.2, 0.1, 0.1])
button = Button(ax_button, "Toplamını Dinle")
button.on_clicked(button_callback)

ax_button2 = plt.axes([0.56, 0.45, 0.2, 0.05])
button2 = Button(ax_button2, "Varsayılan ayarlara dön")
button2.on_clicked(reset)

# Second plot
ax2 = axs[1]
ax2.axis('off')
dosya_yolu = os.path.dirname(os.path.abspath(__file__))
dosya_adi = dosya_yolu + '\\reset.png'
img = plt.imread(dosya_adi)
ax2.imshow(img)

# Adding labels

text25 = ax2.text(0., 700, "0.05", fontsize=12, ha='center')

def button_callsignal(event, signal):
    
    play_sound(signal)
    

ax_button = plt.axes([0.521, 0.05, 0.05, 0.05])
buttons1 = Button(ax_button, "-1-")
buttons1.on_clicked(lambda event: button_callsignal(event, sessignal1))

ax_button = plt.axes([0.597, 0.05, 0.05, 0.05])
buttons2 = Button(ax_button, "-2-")
buttons2.on_clicked(lambda event: button_callsignal(event, sessignal2))

ax_button = plt.axes([0.673, 0.05, 0.05, 0.05])
buttons3 = Button(ax_button, "-3-")
buttons3.on_clicked(lambda event: button_callsignal(event, sessignal3))

ax_button = plt.axes([0.749, 0.05, 0.05, 0.05])
buttons4 = Button(ax_button, "-4-")
buttons4.on_clicked(lambda event: button_callsignal(event, sessignal4))

ax_button = plt.axes([0.825, 0.05, 0.05, 0.05])
buttons5 = Button(ax_button, "-5-")
buttons5.on_clicked(lambda event: button_callsignal(event, sessignal5))

ax_button = plt.axes([0.901, 0.05, 0.05, 0.05])
buttons6 = Button(ax_button, "-6-")
buttons6.on_clicked(lambda event: button_callsignal(event, sessignal6))

text50 = ax2.text(150, 700, "0.1", fontsize=12, ha='center')
text100 = ax2.text(300, 700, "2", fontsize=12, ha='center')
text200 = ax2.text(450, 700, "20", fontsize=12, ha='center')
text400 = ax2.text(600, 700, "40", fontsize=12, ha='center')
text800 = ax2.text(750, 700, "0", fontsize=12, ha='center')
textler = [text25,text50,text100,text200,text400,text800]

# grafiği göster.
plt.show()