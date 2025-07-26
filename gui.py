import tkinter as tk
import threading
import queue
from tkinter import ttk, filedialog
from downloader import descargar_video

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("YouTube Downloader")
    ventana.geometry("500x400")
    ventana.resizable(False, False)

    ruta_destino = tk.StringVar()
    mensaje_estado = tk.StringVar()
    progreso = tk.DoubleVar()
    progreso_queue = queue.Queue()  # NUEVA COLA

    # URL
    ttk.Label(ventana, text="URL del vídeo:").pack(pady=(10, 0))
    entrada_url = ttk.Entry(ventana, width=60)
    entrada_url.pack(pady=5)

    var_audio = tk.BooleanVar()
    def actualizar_estado_calidad():
        selector_calidad.configure(state="disabled" if var_audio.get() else "readonly")
    ttk.Checkbutton(ventana, text="Solo descargar audio", variable=var_audio, command=actualizar_estado_calidad).pack(pady=5)

    # Quality
    ttk.Label(ventana, text="Calidad del vídeo:").pack()
    opciones_calidad = {
        "Máxima disponible (4K o más)": "bestvideo+bestaudio/best",
        "Alta (1080p)": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "Media (720p)": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "Baja (480p)": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "Muy baja (360p)": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    }
    var_calidad = tk.StringVar(value="Media (720p)")
    selector_calidad = ttk.Combobox(ventana, textvariable=var_calidad, values=list(opciones_calidad.keys()), state="readonly")
    selector_calidad.pack(pady=5)

    # Folder
    def seleccionar_carpeta():
        ruta = filedialog.askdirectory()
        if ruta:
            ruta_destino.set(ruta)
            etiqueta_carpeta.config(text=f"Carpeta: {ruta}")
    ttk.Button(ventana, text="Elegir carpeta destino", command=seleccionar_carpeta).pack()
    etiqueta_carpeta = ttk.Label(ventana, text="Carpeta: no seleccionada", foreground="gray")
    etiqueta_carpeta.pack()

    # Progress
    ttk.Label(ventana, text="Progreso:").pack(pady=(10, 0))
    barra = ttk.Progressbar(ventana, orient="horizontal", length=400, mode="determinate", variable=progreso, maximum=100)
    barra.pack(pady=5)
    etiqueta_pct = ttk.Label(ventana, text="0%")
    etiqueta_pct.pack()

    # Status
    etiqueta_estado = ttk.Label(ventana, textvariable=mensaje_estado, foreground="green")
    etiqueta_estado.pack()

    # Download
    def on_descargar():
        url = entrada_url.get()
        solo_audio = var_audio.get()
        destino = ruta_destino.get()
        mensaje_estado.set("")
        progreso.set(0)
        calidad_seleccionada = opciones_calidad[var_calidad.get()]

        if not destino:
            etiqueta_carpeta.config(text="⚠️ Selecciona una carpeta", foreground="red")
            return

        def actualizar_progreso(pct):
            progreso_queue.put(pct)

        def notificar_estado(texto):
            mensaje_estado.set(texto)

        def ejecutar_descarga():
            descargar_video(url, solo_audio, destino, actualizar_progreso, notificar_estado, calidad_seleccionada)

        threading.Thread(target=ejecutar_descarga, daemon=True).start()

    ttk.Button(ventana, text="Descargar", command=on_descargar).pack(pady=10)

    def chequear_progreso():
        try:
            while True:
                pct = progreso_queue.get_nowait()
                print(f"[PROGRESO] {pct}%")
                progreso.set(pct)
                barra['value'] = pct
                etiqueta_pct.config(text=f"{pct:.1f}%")
                barra.update_idletasks()
        except queue.Empty:
            pass
        ventana.after(100, chequear_progreso)

    chequear_progreso()
    ventana.mainloop()
