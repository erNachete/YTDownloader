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
    ventana.geometry("700x520")  # Increased height for all elements to fit
    ventana.resizable(False, False)

    # Set window icon if available (for both taskbar and window corner)
    import sys
    import os

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(__file__), relative_path)

    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            ventana.iconbitmap(default=icon_path)
        except Exception:
            pass

    # Center the window on the screen
    ventana.update_idletasks()
    width = 700
    height = 520
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{x}+{y}")

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

    # --- Download List Section ---
    frame_lista = ttk.LabelFrame(ventana, text="Download List")
    frame_lista.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
    ventana.grid_rowconfigure(3, weight=0)
    ventana.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(frame_lista, columns=("title", "status"), show="headings", height=3)
    tree.heading("title", text="Title")
    tree.heading("status", text="Status")
    tree.column("title", width=400)
    tree.column("status", width=120)
    tree.grid(row=0, column=0, sticky="nsew")
    frame_lista.grid_rowconfigure(0, weight=1)
    frame_lista.grid_columnconfigure(0, weight=1)

    # Dict to keep track of video statuses by yt-dlp id or title
    download_status = {}

    # --- Progress Section ---
    # Section for showing download progress
    frame_progreso = ttk.LabelFrame(ventana, text="Progress")
    frame_progreso.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="we")
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
    boton_descargar = ttk.Button(
        frame_estado,
        text="Download",
        command=lambda: on_descargar(),
        width=20  # Fixed width for the button
    )
    boton_descargar.grid(row=0, column=0, pady=10, padx=5, sticky="w")
    etiqueta_estado = ttk.Label(frame_estado, textvariable=mensaje_estado, foreground="green", width=70, anchor="w")
    etiqueta_estado.grid(row=1, column=0, sticky="w", padx=5)

    # --- Download List Section ---
    frame_lista = ttk.LabelFrame(ventana, text="Download List")
    frame_lista.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(frame_lista, columns=("title", "status"), show="headings", height=7)
    tree.heading("title", text="Title")
    tree.heading("status", text="Status")
    tree.column("title", width=400)
    tree.column("status", width=120)
    tree.grid(row=0, column=0, sticky="nsew")
    frame_lista.grid_rowconfigure(0, weight=1)
    frame_lista.grid_columnconfigure(0, weight=1)

    # Dict to keep track of video statuses by yt-dlp id or title
    download_status = {}

    # --- Download and progress logic ---
    def on_descargar():
        """
        Handles the download button click event.
        Starts the download in a separate thread and manages progress updates.
        Checks if the output file already exists before downloading.
        Supports both single videos and playlists.
        """
        url = entrada_url.get()
        solo_audio = var_audio.get()
        destino = ruta_destino.get()
        mensaje_estado.set("")
        progreso.set(0)
        calidad_seleccionada = opciones_calidad[var_calidad.get()]
        formato_seleccionado = var_formato.get()

        import os
        from yt_dlp.utils import sanitize_filename

        # Get info for playlist, channel, or single video
        video_entries = []
        is_playlist_or_channel = False
        try:
            from yt_dlp import YoutubeDL
            with YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                # Accept both playlist and channel as multi-video containers
                if info.get('_type') in ('playlist', 'channel', 'multi_video'):
                    is_playlist_or_channel = True
                    video_entries = info.get('entries', [])
                else:
                    video_entries = [info]
        except Exception:
            video_entries = []

        # Clear previous list
        for i in tree.get_children():
            tree.delete(i)
        download_status.clear()

        # Populate the list with pending status
        if video_entries:
            # Flatten nested entries (e.g., channels with "videos", "shorts", "streams" sections)
            flat_entries = []
            for entry in video_entries:
                # If entry is a section (e.g., "videos", "shorts", "streams"), flatten its entries
                if isinstance(entry, dict) and entry.get('_type') == 'playlist' and 'entries' in entry:
                    for subentry in entry['entries']:
                        flat_entries.append(subentry)
                else:
                    flat_entries.append(entry)
            for idx, entry in enumerate(flat_entries):
                title = entry.get('title', 'Unknown')
                vid = entry.get('id', None)
                iid = f"{vid or 'video'}_{idx}"
                if not tree.exists(iid):
                    tree.insert('', 'end', iid=iid, values=(title, "pending"))
                download_status[iid] = "pending"
                entry['_tree_iid'] = iid
            # Replace video_entries with the flattened list for the download logic
            video_entries = flat_entries
        else:
            # Fallback for unknown/invalid url
            if not tree.exists("single"):
                tree.insert('', 'end', iid="single", values=("Unknown", "pending"))
            download_status["single"] = "pending"

        # For playlist or channel, skip file existence check and download all

        def actualizar_progreso(pct, vid=None):
            # Print progress for debugging
            print(f"[GUI] Progress: {pct}% (vid={vid})")
            progreso_queue.put(pct)
            if vid and vid in download_status:
                tree.set(vid, "status", "downloading")
                download_status[vid] = "downloading"

        def notificar_estado(texto, vid=None):
            print(f"[GUI] Status: {texto} (vid={vid})")
            mensaje_estado.set(texto)
            if vid and vid in download_status:
                if "completed" in texto.lower():
                    tree.set(vid, "status", "completed")
                    download_status[vid] = "completed"
                    # Scroll to the completed item
                    tree.see(vid)
                elif "error" in texto.lower():
                    tree.set(vid, "status", "error")
                    download_status[vid] = "error"
                    tree.see(vid)

        def ejecutar_descarga():
            # For playlist or channel, download each entry and update status
            if is_playlist_or_channel and video_entries:
                for entry in video_entries:
                    title = entry.get('title', 'Unknown')
                    iid = entry.get('_tree_iid', None)
                    if not iid or not tree.exists(iid):
                        continue  # Skip if not in the tree
                    tree.set(iid, "status", "downloading")
                    download_status[iid] = "downloading"
                    def prog(pct, v=iid):
                        actualizar_progreso(pct, v)
                    def estado(txt, v=iid):
                        notificar_estado(txt, v)
                    try:
                        descargar_video(
                            entry.get('url', url),
                            solo_audio,
                            destino,
                            prog,
                            estado,
                            calidad_seleccionada,
                            formato_seleccionado
                        )
                        tree.set(iid, "status", "completed")
                        download_status[iid] = "completed"
                    except Exception:
                        tree.set(iid, "status", "error")
                        download_status[iid] = "error"
            else:
                # Single video
                vid = video_entries[0].get('id', "single") if video_entries else "single"
                iid = f"{vid}_0" if video_entries else "single"
                if tree.exists(iid):
                    tree.set(iid, "status", "downloading")
                    download_status[iid] = "downloading"
                def prog(pct, v=iid):
                    actualizar_progreso(pct, v)
                def estado(txt, v=iid):
                    notificar_estado(txt, v)
                try:
                    descargar_video(
                        url,
                        solo_audio,
                        destino,
                        prog,
                        estado,
                        calidad_seleccionada,
                        formato_seleccionado
                    )
                    if tree.exists(iid):
                        tree.set(iid, "status", "completed")
                        download_status[iid] = "completed"
                except Exception:
                    if tree.exists(iid):
                        tree.set(iid, "status", "error")
                        download_status[iid] = "error"

        threading.Thread(target=ejecutar_descarga, daemon=True).start()

    def chequear_progreso():
        """
        Periodically checks the progress queue and updates the progress bar and label.
        """
        try:
            while True:
                pct = progreso_queue.get_nowait()
                progreso.set(pct)
                barra['value'] = pct
                etiqueta_pct.config(text=f"{pct:.1f}%")
                barra.update_idletasks()
        except queue.Empty:
            pass
        ventana.after(100, chequear_progreso)

    chequear_progreso()
    ventana.mainloop()
