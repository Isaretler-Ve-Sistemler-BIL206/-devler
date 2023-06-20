import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

defaultFilePath = "Bozdogan_Turkusu_Ittihat_ve_Terakki_kesit.wav"

def play_audio(data, sample_rate):
    sd.play(data, sample_rate)
    sd.wait()

# Filtre parametreleri
cutoff_freq = 100 # Kesim frekansı (Hz)
order = 4  # Filtre sırası

# Lowpass (Alçak geçiren) filtre
def lowpass_filter(data, cutoff, fs, order):
    # Butterworth alçak geçiren filtre için katsayıları hesapla
    # order: Filtre sırası, cutoff: Kesme frekansı, fs: Örnekleme frekansı
    lowpass_b, lowpass_a = signal.butter(order, cutoff, fs=fs, btype='lowpass')

    # Filtreleme işlemini gerçekleştir
    filtered_data = signal.lfilter(lowpass_b, lowpass_a, data, axis=0)

    # Filtrelenmiş veriyi döndür
    return filtered_data


# Highpass (Yüksek geçiren) filtre
def highpass_filter(data, cutoff, fs, order):
    # Butterworth yüksek geçiren filtre için katsayıları hesapla
    # order: Filtre sırası, cutoff: Kesme frekansı, fs: Örnekleme frekansı
    highpass_b, highpass_a = signal.butter(order, cutoff, fs=fs, btype='highpass')

    # Filtreleme işlemini gerçekleştir
    filtered_data = signal.lfilter(highpass_b, highpass_a, data, axis=0)

    # Filtrelenmiş veriyi döndür
    return filtered_data


# Bandpass (Band geçiren) filtre
def bandpass_filter(data, low_freq, high_freq, fs, order):
    # Butterworth band geçiren filtre için katsayıları hesapla
    # order: Filtre sırası, [low_freq, high_freq]: Kesme frekansları, fs: Örnekleme frekansı
    bandpass_b, bandpass_a = signal.butter(order, [low_freq, high_freq], fs=fs, btype='bandpass')

    # Filtreleme işlemini gerçekleştir
    filtered_data = signal.lfilter(bandpass_b, bandpass_a, data, axis=0)

    # Filtrelenmiş veriyi döndür
    return filtered_data


# Ses dosyasını filtreye sokup grafikleri oluşturan fonksiyon
def filter_and_plot(file_path, cutoff_freq, order):
    # Ses dosyasını yükleme
    ses_dosyasi, orneklem_hizi = sf.read(file_path)

    # Lowpass filtreleme
    global ses_lowpass
    ses_lowpass = lowpass_filter(ses_dosyasi, cutoff_freq, orneklem_hizi, order)

    # Highpass filtreleme
    global ses_highpass 
    ses_highpass = highpass_filter(ses_dosyasi, cutoff_freq, orneklem_hizi, order)

    # Bandpass filtreleme
    global ses_bandpass
    bandpass_low = cutoff_freq - 0
    bandpass_high = cutoff_freq + 300
    ses_bandpass = bandpass_filter(ses_dosyasi, bandpass_low, bandpass_high, orneklem_hizi, order)

    # Zaman dizisi
    zaman = np.arange(0, len(ses_dosyasi)) / orneklem_hizi

    ############################################################################
    ########## 82 - 331. SATIRLAR ARASI ARAYUZ WIDGETLARINI ICERIYOR ##########
    ############################################################################

    # Tkinter formunu oluşturma
    root = tk.Tk()
    root.title("Ses Filtreleme ve Grafikleme")

    # Grid yöneticisini kullanarak frameleri yerleştir
    frame1 = tk.Frame(root, bg="white")
    frame2 = tk.Frame(root, bg="white")
    frame3 = tk.Frame(root, bg="white")
    frame4 = tk.Frame(root, bg="white")

    frame1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    frame2.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
    frame3.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
    frame4.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")

    # Ek frameleri oluştur
    frame5 = tk.Frame(root, bg="white", width=frame1.winfo_width(), height=40)
    frame6 = tk.Frame(root, bg="white", width=frame2.winfo_width(), height=40)
    frame7 = tk.Frame(root, bg="white", width=frame3.winfo_width(), height=40)
    frame8 = tk.Frame(root, bg="white", width=frame4.winfo_width(), height=40)

    # Ek frameleri grid yöntemiyle yerleştir
    frame5.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
    frame6.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
    frame7.grid(row=3, column=0, padx=0, pady=0, sticky="nsew")
    frame8.grid(row=3, column=1, padx=0, pady=0, sticky="nsew")

    # Grid yöneticisine özel boyut ayarları
    root.columnconfigure(0, weight=1, minsize=600)
    root.columnconfigure(1, weight=1, minsize=600)
    root.rowconfigure(0, weight=1, minsize=200)
    root.rowconfigure(2, weight=1, minsize=200)

    # Grafikleri her bir frame'e yerleştir
    # Grafik oluşturma
    def figure_original(zaman, ses_dosyasi, frame):
        # 7x3 boyutunda bir figür oluşturuluyor.
        fig1 = plt.figure(figsize=(7, 3))
        # 1x1 alt grafiği figüre ekleniyor.
        ax1 = fig1.add_subplot(111)
        # Grafikteki öğeler arasındaki boşluklar ayarlanıyor.
        fig1.tight_layout(pad=4, h_pad=2, w_pad=4)
        
        # Zaman ve ses dosyası verileri kullanılarak bir çizgi grafiği çiziliyor.
        ax1.plot(zaman, ses_dosyasi, color='purple')
        # Grafik başlığı ayarlanıyor.
        ax1.set_title('Orjinal Ses')
        # X ekseninin etiketi ayarlanıyor.
        ax1.set_xlabel('Zaman (s)')
        # Y ekseninin etiketi ayarlanıyor.
        ax1.set_ylabel('Amplitüd')

        # Çizilen grafiği bir Tkinter penceresinde görüntülemek için bir FigureCanvasTkAgg nesnesi oluşturuluyor.
        canvas1 = FigureCanvasTkAgg(fig1, master=frame)
        # Canvas çizimleri yapılıyor.
        canvas1.draw()
        # Tkinter penceresindeki widget'a yerleştiriliyor.
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def figure_lowpass(zaman, ses_dosyasi, cutoff, frame):
        # Eski grafiği sil
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Lowpass filtreleme
        global ses_lowpass
        ses_lowpass = lowpass_filter(ses_dosyasi, cutoff, orneklem_hizi, order)
        # 7x3 boyutunda bir figür oluşturuluyor.
        fig2 = plt.figure(figsize=(7, 3))
        # 1x1 alt grafiği figüre ekleniyor.
        ax2 = fig2.add_subplot(111)
        # Grafikteki öğeler arasındaki boşluklar ayarlanıyor.
        fig2.tight_layout(pad=4, h_pad=2, w_pad=4)

        # Lowpass filtrelenmiş ses dosyasını kırmızı renkte bir çizgi grafiği olarak çiz
        ax2.plot(zaman, ses_lowpass, color='red')
        # Orjinal ses dosyasını siyah renkte, yarı saydamlık ayarlanmış bir çizgi grafiği olarak çiz
        ax2.plot(zaman, ses_dosyasi, color='black', alpha=0.5)
        # Grafik başlığı ayarlanıyor.
        ax2.set_title(f'Lowpass Ses (Kesim Frekansı: {cutoff} Hz)')
        # X ekseninin etiketi ayarlanıyor.
        ax2.set_xlabel('Zaman (s)')
        # Y ekseninin etiketi ayarlanıyor.
        ax2.set_ylabel('Amplitüd')

        # Çizilen grafikleri bir Tkinter penceresinde görüntülemek için bir FigureCanvasTkAgg nesnesi oluşturuluyor.
        canvas2 = FigureCanvasTkAgg(fig2, master=frame)
        # Canvas çizimleri yapılıyor.
        canvas2.draw()
        # Tkinter penceresindeki widget'a yerleştiriliyor.
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def figure_highpass(zaman, ses_dosyasi, cutoff, frame):
        # Çerçevedeki önceki widget'ları sil
        for widget in frame.winfo_children():
            widget.destroy()        
        
        # Highpass filtreleme işlemi
        global ses_highpass
        ses_highpass = highpass_filter(ses_dosyasi, cutoff, orneklem_hizi, order)
        
        # 7x3 boyutunda bir figür oluşturuluyor.
        fig3 = plt.figure(figsize=(7, 3))
        # 1x1 alt grafiği figüre ekleniyor.
        ax3 = fig3.add_subplot(111)
        # Grafikteki öğeler arasındaki boşluklar ayarlanıyor.
        fig3.tight_layout(pad=4, h_pad=2, w_pad=4)

        # Highpass filtrelenmiş ses dosyasını kırmızı renkte bir çizgi grafiği olarak çiz
        ax3.plot(zaman, ses_highpass, color='red')
        # Orjinal ses dosyasını siyah renkte, yarı saydamlık ayarlanmış bir çizgi grafiği olarak çiz
        ax3.plot(zaman, ses_dosyasi, color='black', alpha=0.5)
        # Grafik başlığı ayarlanıyor.
        ax3.set_title(f'Highpass Ses (Kesim Frekansı: {cutoff} Hz)')
        # X ekseninin etiketi ayarlanıyor.
        ax3.set_xlabel('Zaman (s)')
        # Y ekseninin etiketi ayarlanıyor.
        ax3.set_ylabel('Amplitüd')

        # Çizilen grafikleri bir Tkinter penceresinde görüntülemek için bir FigureCanvasTkAgg nesnesi oluşturuluyor.
        canvas3 = FigureCanvasTkAgg(fig3, master=frame)
        # Canvas çizimleri yapılıyor.
        canvas3.draw()
        # Tkinter penceresindeki widget'a yerleştiriliyor.
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def figure_bandpass(zaman, ses_dosyasi, low, high, frame):
        # Eski grafiği sil
        for widget in frame.winfo_children():
            widget.destroy()          
        
        # Bandpass filtreleme
        global ses_bandpass
        bandpass_low = low
        bandpass_high = high
        ses_bandpass = bandpass_filter(ses_dosyasi, bandpass_low, bandpass_high, orneklem_hizi, order)    
        
        # 7x3 boyutunda bir figür oluşturuluyor.
        fig4 = plt.figure(figsize=(7, 3))
        # 1x1 alt grafiği figüre ekleniyor.
        ax4 = fig4.add_subplot(111)
        # Grafikteki öğeler arasındaki boşluklar ayarlanıyor.
        fig4.tight_layout(pad=4, h_pad=2, w_pad=4)

        # Bandpass filtrelenmiş ses dosyasını kırmızı renkte bir çizgi grafiği olarak çiz
        ax4.plot(zaman, ses_bandpass, color='red')
        # Orjinal ses dosyasını siyah renkte, yarı saydamlık ayarlanmış bir çizgi grafiği olarak çiz
        ax4.plot(zaman, ses_dosyasi, color='black', alpha=0.5)
        # Grafik başlığı ayarlanıyor.
        ax4.set_title(f'Bandpass Ses (Alt Kesim Frekansı: {bandpass_low} Hz, Üst Kesim Frekansı: {bandpass_high} Hz)')
        # X ekseninin etiketi ayarlanıyor.
        ax4.set_xlabel('Zaman (s)')
        # Y ekseninin etiketi ayarlanıyor.
        ax4.set_ylabel('Amplitüd')

        # Çizilen grafikleri bir Tkinter penceresinde görüntülemek için bir FigureCanvasTkAgg nesnesi oluşturuluyor.
        canvas4 = FigureCanvasTkAgg(fig4, master=frame)
        # Canvas çizimleri yapılıyor.
        canvas4.draw()
        # Tkinter penceresindeki widget'a yerleştiriliyor.
        canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    figure_original(zaman, ses_dosyasi, frame1)

    figure_lowpass(zaman, ses_dosyasi, cutoff_freq, frame2)

    figure_highpass(zaman, ses_dosyasi, cutoff_freq, frame3)

    figure_bandpass(zaman, ses_dosyasi, bandpass_low, bandpass_high, frame4)



    # ses çalma butonları için işlevler
    def play_lowpass():
        play_audio(ses_lowpass, orneklem_hizi)

    def play_highpass():
        play_audio(ses_highpass, orneklem_hizi)

    def play_bandpass():
        play_audio(ses_bandpass, orneklem_hizi)

    def play_originalsound():
        play_audio(ses_dosyasi, orneklem_hizi)

    # ses çalma buttonları oluşturma
    button_originalsound = tk.Button(frame5, text="Çal", bg='#283241', fg='white', width=10, activebackground='green', activeforeground='white', command=play_originalsound)
    button_lowpass = tk.Button(frame6, text="Çal", bg='#283241', fg='white', width=10, activebackground='green', activeforeground='white', command=play_lowpass)
    button_highpass = tk.Button(frame7, text="Çal", bg='#283241', fg='white', width=10, activebackground='green', activeforeground='white', command=play_highpass)
    button_bandpass = tk.Button(frame8, text="Çal", bg='#283241', fg='white', width=10, activebackground='green', activeforeground='white', command=play_bandpass)

    # Buttonları frame'lere yerleştirme
    button_originalsound.pack(side=tk.LEFT, padx=20, pady=5)
    button_lowpass.pack(side=tk.RIGHT, padx=20, pady=5)
    button_highpass.pack(side=tk.RIGHT, padx=20, pady=5)
    button_bandpass.pack(side=tk.RIGHT, padx=20, pady=5)

    # ses dosyasının maksimum frekansı
    max_frequency = orneklem_hizi / 2
    
    # Scale nesnelerini oluşturma
    scale_lowpass = tk.Scale(frame6, from_=1, to=max_frequency, length=350, resolution=1, orient=tk.HORIZONTAL)
    scale_highpass = tk.Scale(frame7, from_=1, to=max_frequency, length=350, resolution=1, orient=tk.HORIZONTAL)
    scale_bandpass1 = tk.Scale(frame8, from_=1, to=max_frequency, length=150, resolution=1, orient=tk.HORIZONTAL)
    scale_bandpass2 = tk.Scale(frame8, from_=1, to=max_frequency, length=150, resolution=1, orient=tk.HORIZONTAL)

    # Label nesnelerini oluşturma
    label_lowpass = tk.Label(frame6, text="Lowpass:", bg="white")
    label_highpass = tk.Label(frame7, text="Highpass:", bg="white")
    label_bandpass1 = tk.Label(frame8, text="Bandpass - Alt:", bg="white")
    label_bandpass_void = tk.Label(frame8, text=" ", bg="white")
    label_bandpass2 = tk.Label(frame8, text="Bandpass - Üst:", bg="white")

    # Güncelleme Buttonlarıiçin işlevler
    def lowpass_ref():
        figure_lowpass(zaman, ses_dosyasi, scale_lowpass.get(), frame2)

    def highpass_ref():
        figure_highpass(zaman, ses_dosyasi, scale_highpass.get(), frame3)

    def bandpass_ref():
        figure_bandpass(zaman, ses_dosyasi, scale_bandpass1.get(), scale_bandpass2.get(), frame4)

    # Güncelleme Buttonlarını oluşturma
    button_lowpass_refresh = tk.Button(frame6, text="Güncelle", activebackground='green', activeforeground='white', command=lowpass_ref)
    button_highpass_refresh = tk.Button(frame7, text="Güncelle", activebackground='green', activeforeground='white', command=highpass_ref)
    button_bandpass_refresh = tk.Button(frame8, text="Güncelle", activebackground='green', activeforeground='white', command=bandpass_ref)


    # Button, Scale ve Label nesnelerini yerleştirme
    label_lowpass.pack(side=tk.LEFT, padx=2, pady=10)
    scale_lowpass.pack(side=tk.LEFT, padx=2, pady=10)
    label_highpass.pack(side=tk.LEFT, padx=2, pady=10)
    scale_highpass.pack(side=tk.LEFT, padx=2, pady=10)
    label_bandpass1.pack(side=tk.LEFT, padx=2, pady=10)
    scale_bandpass1.pack(side=tk.LEFT, padx=2, pady=10)
    label_bandpass_void.pack(side=tk.LEFT, padx=10, pady=10)
    label_bandpass2.pack(side=tk.LEFT, padx=2, pady=10)
    scale_bandpass2.pack(side=tk.LEFT, padx=2, pady=10)

    button_lowpass_refresh.pack(side=tk.LEFT, padx=2, pady=10)
    button_highpass_refresh.pack(side=tk.LEFT, padx=2, pady=10)
    button_bandpass_refresh.pack(side=tk.LEFT, padx=2, pady=10)


    # Tkinter formunu çalıştırma
    root.mainloop()


# bir tkinter formu oluşturur ve forma iki adet buton ekler:
    # birinci buton analiz ve filtreleme yapmak için bir ses dosyası seçim ekranı sunar.
    # ikinci buton bizim eklediğimiz 9sn uzunluğunda varsayılan ses dosyasının analiz edilmesini sağlar.
def start_form():
    # Formu oluştur
    form = tk.Tk()
    form.title("Ses Filtreleme ve Grafikleme")
    form.geometry("500x400")

    # Formun arka plan rengini ayarla
    form.configure(bg="#ffffff")

    # Frame oluştur
    ust_frame = tk.Frame(form, bg="#ffffff")
    ust_frame.pack(fill=tk.BOTH, ipady=10)

    # Başlık etiketi
    baslik = tk.Label(ust_frame, text="ÖDEV6 (DÖNEM SONU ÖDEVİ)", bg="#ffffff", fg="#0d1117", font=("Arial", 20, "bold"))
    baslik.pack(padx=10, pady=20)

    baslikalt = tk.Label(ust_frame, text="KONUŞMA/MÜZİK SESİ ÜZERİNDE FARKLI FİLTRELEME UYGULAMALARI", bg="#ffffff", fg="#0d1117", font=("Arial", 10, "italic"))
    baslikalt.pack(padx=10, pady=5)

    # Butonlar
    # Ses dosyası seçme butonunun işlevi
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("WAV Dosyaları", "*.wav")])
        if file_path:
            # Filtreleme ve grafikleri oluşturma
            filter_and_plot(file_path, cutoff_freq, order)
            # Matplotlib figürünü güncelleme

    # Ses dosyası seçme butonu
    button_select = tk.Button(form, text="Ses Dosyası Seç", bg="#283241", fg="#fafbff", relief="flat", width=30, height=5, command=select_file)
    button_select.config(font=("Arial", 14)) 

    # Butonu forma yerleştir
    button_select.pack(pady=30)

        # varsayılan ses dosyası ile başlatma butonu
    # varsayılan ses dosyası ile başlatma buton işlevi
    def button_default_click():
        filter_and_plot(defaultFilePath, cutoff_freq, order)

    button_default = tk.Button(form, text="Varsayılan dosya", bg="#283241", fg="#fafbff", relief="flat", width=30, command=button_default_click)

    # Butonu forma yerleştir
    button_default.pack(pady=30)

    form.mainloop()

start_form()