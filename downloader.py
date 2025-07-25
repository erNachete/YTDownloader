from yt_dlp import YoutubeDL
import os

def descargar_video(url: str, solo_audio: bool, destino: str, callback_progreso=None, callback_estado=None):
    print(f"[DEBUG] Descargando: {url} | Solo audio: {solo_audio} | Carpeta: {destino}")

    def hook(d):
        if d['status'] == 'downloading' and callback_progreso:
            porcentaje = d.get('_percent_str', '0%').strip().replace('%', '')
            try:
                callback_progreso(float(porcentaje))
            except ValueError:
                pass
        elif d['status'] == 'finished':
            if callback_progreso:
                callback_progreso(100)
            if callback_estado:
                callback_estado("✅ ¡Descarga completada!")

    opciones = {
        'format': 'bestaudio/best' if solo_audio else 'best',
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
        'progress_hooks': [hook],
        'quiet': True,
    }

    with YoutubeDL(opciones) as ydl:
        ydl.download([url])
