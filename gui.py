import tkinter as tk
from tkinter import ttk, filedialog
from downloader import descargar_video

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Descargador de YouTube")
    ventana.geometry("500x250")
    ventana.resizable(False, False)

    ruta_destino = tk.StringVar(value="")

    # URL
    ttk.Label(ventana, text="URL del vídeo:").pack(pady=(10, 0))
    entrada_url = ttk.Entry(ventana, width=60)
    entrada_url.pack(pady=5)

    # Solo audio
    var_audio = tk.BooleanVar()
    check_audio = ttk.Checkbutton(ventana, text="Solo descargar audio", variable=var_audio)
    check_audio.pack(pady=5)

    # Selector de carpeta
    def seleccionar_carpeta():
        ruta = filedialog.askdirectory()
        if ruta:
            ruta_destino.set(ruta)
            etiqueta_carpeta.config(text=f"Carpeta: {ruta}")

    ttk.Button(ventana, text="Elegir carpeta destino", command=seleccionar_carpeta).pack(pady=5)
    etiqueta_carpeta = ttk.Label(ventana, text="Carpeta: no seleccionada", foreground="gray")
    etiqueta_carpeta.pack()

    # Botón de descarga
    def on_descargar():
        url = entrada_url.get()
        solo_audio = var_audio.get()
        destino = ruta_destino.get()
        if not destino:
            etiqueta_carpeta.config(text="⚠️ Selecciona una carpeta antes de descargar", foreground="red")
            return
        descargar_video(url, solo_audio, destino)

    ttk.Button(ventana, text="Descargar", command=on_descargar).pack(pady=10)

    ventana.mainloop()
