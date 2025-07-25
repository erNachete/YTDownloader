from yt_dlp import YoutubeDL
import os

def descargar_video(url: str, solo_audio: bool, destino: str):
    print(f"[DEBUG] Descargando: {url} | Solo audio: {solo_audio} | Carpeta: {destino}")

    opciones = {
        'format': 'bestaudio/best' if solo_audio else 'best',
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
    }

    with YoutubeDL(opciones) as ydl:
        ydl.download([url])
