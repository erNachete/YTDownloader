import tkinter as tk
from tkinter import ttk, filedialog
from downloader import descargar_video

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Descargador de YouTube")
    ventana.geometry("500x300")
    ventana.resizable(False, False)

    ruta_destino = tk.StringVar(value="")
    mensaje_estado = tk.StringVar(value="")
    progreso = tk.DoubleVar(value=0)

    # URL
    ttk.Label(ventana, text="URL del vídeo:").pack(pady=(10, 0))
    entrada_url = ttk.Entry(ventana, width=60)
    entrada_url.pack(pady=5)

    # Solo audio
    var_audio = tk.BooleanVar()
    ttk.Checkbutton(ventana, text="Solo descargar audio", variable=var_audio).pack(pady=5)

    # Carpeta destino
    def seleccionar_carpeta():
        ruta = filedialog.askdirectory()
        if ruta:
            ruta_destino.set(ruta)
            etiqueta_carpeta.config(text=f"Carpeta: {ruta}")

    ttk.Button(ventana, text="Elegir carpeta destino", command=seleccionar_carpeta).pack(pady=5)
    etiqueta_carpeta = ttk.Label(ventana, text="Carpeta: no seleccionada", foreground="gray")
    etiqueta_carpeta.pack()

    # Barra de progreso
    ttk.Label(ventana, text="Progreso:").pack(pady=(10, 0))
    barra = ttk.Progressbar(ventana, orient="horizontal", length=400, mode="determinate", variable=progreso)
    barra.pack(pady=5)

    # Mensaje final
    etiqueta_estado = ttk.Label(ventana, textvariable=mensaje_estado, foreground="green")
    etiqueta_estado.pack()

    # Botón de descarga
    def on_descargar():
        url = entrada_url.get()
        solo_audio = var_audio.get()
        destino = ruta_destino.get()
        mensaje_estado.set("")
        progreso.set(0)

        if not destino:
            etiqueta_carpeta.config(text="⚠️ Selecciona una carpeta antes de descargar", foreground="red")
            return

        def actualizar_progreso(pct):
            progreso.set(pct)

        def notificar_estado(texto):
            mensaje_estado.set(texto)

        descargar_video(url, solo_audio, destino, actualizar_progreso, notificar_estado)

    ttk.Button(ventana, text="Descargar", command=on_descargar).pack(pady=10)

    ventana.mainloop()
