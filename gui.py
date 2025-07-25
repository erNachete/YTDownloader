import tkinter as tk
from tkinter import ttk
from downloader import descargar_video

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Descargador de YouTube")
    ventana.geometry("400x200")
    ventana.resizable(False, False)

    # URL
    ttk.Label(ventana, text="URL del vídeo:").pack(pady=(10, 0))
    entrada_url = ttk.Entry(ventana, width=50)
    entrada_url.pack(pady=5)

    # Checkbox: solo audio
    var_audio = tk.BooleanVar()
    check_audio = ttk.Checkbutton(ventana, text="Solo descargar audio", variable=var_audio)
    check_audio.pack(pady=5)

    # Botón de descarga
    def on_descargar():
        url = entrada_url.get()
        solo_audio = var_audio.get()
        descargar_video(url, solo_audio)

    boton_descargar = ttk.Button(ventana, text="Descargar", command=on_descargar)
    boton_descargar.pack(pady=10)

    ventana.mainloop()
