import tkinter as tk
import threading
import queue
from tkinter import ttk, filedialog
from downloader import descargar_video

def crear_interfaz():
    """
    Initializes and runs the main GUI for the YouTube Downloader application.
    Organizes the interface into logical sections for URL input, download options,
    destination folder selection, progress display, and status messages.
    """
    ventana = tk.Tk()
    ventana.title("YouTube Downloader")
    ventana.geometry("700x480")  # Increased width and height
    ventana.resizable(False, False)

    ruta_destino = tk.StringVar()
    mensaje_estado = tk.StringVar()
    progreso = tk.DoubleVar()
    progreso_queue = queue.Queue()

    # --- URL Section ---
    # Section for entering the video URL
    frame_url = ttk.LabelFrame(ventana, text="Video Link")
    frame_url.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="we")
    ttk.Label(frame_url, text="Video URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entrada_url = ttk.Entry(frame_url, width=80)
    entrada_url.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    # --- Options Section ---
    # Section for download options: audio only, video quality, and format
    frame_opciones = ttk.LabelFrame(ventana, text="Download Options")
    frame_opciones.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="we")

    var_audio = tk.BooleanVar()

    # Format selection
    ttk.Label(frame_opciones, text="Format:").grid(row=1, column=2, sticky="w", padx=(10,0))
    formatos_video = ["mp4", "avi", "mkv", "webm"]
    formatos_audio = ["mp3", "aac", "wav", "m4a", "opus"]
    var_formato = tk.StringVar(value="mp4")
    selector_formato = ttk.Combobox(
        frame_opciones,
        textvariable=var_formato,
        values=formatos_video,
        state="readonly",
        width=15
    )
    selector_formato.grid(row=1, column=3, pady=5, padx=5, sticky="we")

    def actualizar_estado_calidad():
        """
        Enables or disables the video quality dropdown depending on whether
        'Audio only' is selected. Shows a message if only audio is selected.
        Also switches format options between video and audio formats.
        """
        if var_audio.get():
            selector_calidad.configure(state="disabled")
            etiqueta_audio.grid(row=2, column=0, columnspan=4, pady=2, sticky="w")
            selector_formato.configure(state="readonly")
            selector_formato['values'] = formatos_audio
            var_formato.set(formatos_audio[0])
        else:
            selector_calidad.configure(state="readonly")
            etiqueta_audio.grid_remove()
            selector_formato.configure(state="readonly")
            selector_formato['values'] = formatos_video
            var_formato.set(formatos_video[0])
    ttk.Checkbutton(
        frame_opciones,
        text="Audio only",
        variable=var_audio,
        command=actualizar_estado_calidad
    ).grid(row=0, column=0, columnspan=4, pady=5, sticky="w")

    ttk.Label(frame_opciones, text="Video quality:").grid(row=1, column=0, sticky="w")
    opciones_calidad = {
        "Máxima disponible (4K o más)": "bestvideo+bestaudio/best",
        "Alta (1080p)": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "Media (720p)": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "Baja (480p)": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "Muy baja (360p)": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    }
    var_calidad = tk.StringVar(value="Media (720p)")
    selector_calidad = ttk.Combobox(
        frame_opciones,
        textvariable=var_calidad,
        values=list(opciones_calidad.keys()),
        state="readonly",
        width=25
    )
    selector_calidad.grid(row=1, column=1, pady=5, padx=5, sticky="we")

    etiqueta_audio = ttk.Label(
        frame_opciones,
        text="Audio only selected, quality not available",
        foreground="orange"
    )
    etiqueta_audio.grid(row=2, column=0, columnspan=4, pady=2, sticky="w")
    etiqueta_audio.grid_remove()

    # --- Folder Section ---
    # Section for selecting the destination folder
    frame_carpeta = ttk.LabelFrame(ventana, text="Destination Folder")
    frame_carpeta.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="we")
    def seleccionar_carpeta():
        """
        Opens a dialog to select the destination folder and updates the label.
        """
        ruta = filedialog.askdirectory()
        if ruta:
            ruta_destino.set(ruta)
            etiqueta_carpeta.config(text=f"Folder: {ruta}")
    ttk.Button(
        frame_carpeta,
        text="Choose destination folder",
        command=seleccionar_carpeta
    ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    etiqueta_carpeta = ttk.Label(frame_carpeta, text="Folder: not selected", foreground="gray")
    etiqueta_carpeta.grid(row=0, column=1, padx=5, sticky="w")

    # --- Progress Section ---
    # Section for showing download progress
    frame_progreso = ttk.LabelFrame(ventana, text="Progress")
    frame_progreso.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="we")
    barra = ttk.Progressbar(
        frame_progreso,
        orient="horizontal",
        length=600,
        mode="determinate",
        variable=progreso,
        maximum=100
    )
    barra.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky="we")
    etiqueta_pct = ttk.Label(frame_progreso, text="0%")
    etiqueta_pct.grid(row=0, column=3, sticky="w", padx=5)

    # --- Status and Download Section ---
    # Section for status messages and download button
    frame_estado = ttk.LabelFrame(ventana, text="Status")
    frame_estado.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="we")
    etiqueta_estado = ttk.Label(frame_estado, textvariable=mensaje_estado, foreground="green", width=70, anchor="w")
    etiqueta_estado.grid(row=0, column=0, sticky="w", padx=5)
    boton_descargar = ttk.Button(
        frame_estado,
        text="Download",
        command=lambda: on_descargar(),
        width=20  # Fixed width for the button
    )
    boton_descargar.grid(row=1, column=0, pady=10, padx=5, sticky="w")

    # --- Download and progress logic ---
    def on_descargar():
        """
        Handles the download button click event.
        Starts the download in a separate thread and manages progress updates.
        Checks if the output file already exists before downloading.
        """
        url = entrada_url.get()
        solo_audio = var_audio.get()
        destino = ruta_destino.get()
        mensaje_estado.set("")
        progreso.set(0)
        calidad_seleccionada = opciones_calidad[var_calidad.get()]
        formato_seleccionado = var_formato.get()

        # Determine output filename
        import os
        from yt_dlp.utils import sanitize_filename

        # Get title (best effort, fallback to 'output')
        video_title = "output"
        try:
            from yt_dlp import YoutubeDL
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = sanitize_filename(info.get('title', 'output'))
        except Exception:
            pass

        if solo_audio:
            ext = formato_seleccionado
        else:
            ext = formato_seleccionado

        output_file = os.path.join(destino, f"{video_title}.{ext}")

        if os.path.exists(output_file):
            mensaje_estado.set(f"⚠️ File already exists: {output_file}")
            etiqueta_estado.config(foreground="orange")
            return
        else:
            etiqueta_estado.config(foreground="green")

        def actualizar_progreso(pct):
            """
            Callback to update the progress bar from the downloader.
            """
            progreso_queue.put(pct)

        def notificar_estado(texto):
            """
            Callback to update the status message from the downloader.
            """
            mensaje_estado.set(texto)

        def ejecutar_descarga():
            descargar_video(
                url,
                solo_audio,
                destino,
                actualizar_progreso,
                notificar_estado,
                calidad_seleccionada,
                formato_seleccionado
            )
        threading.Thread(target=ejecutar_descarga, daemon=True).start()

    def chequear_progreso():
        """
        Periodically checks the progress queue and updates the progress bar and label.
        """
        try:
            while True:
                pct = progreso_queue.get_nowait()
                print(f"[PROGRESS] {pct}%")
                progreso.set(pct)
                barra['value'] = pct
                etiqueta_pct.config(text=f"{pct:.1f}%")
                barra.update_idletasks()
        except queue.Empty:
            pass
        ventana.after(100, chequear_progreso)

    chequear_progreso()
    ventana.mainloop()
