from yt_dlp import YoutubeDL

def descargar_video(url: str, solo_audio: bool):
    print(f"[DEBUG] Iniciando descarga: {url} | Solo audio: {solo_audio}")

    opciones = {
        'format': 'bestaudio/best' if solo_audio else 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    with YoutubeDL(opciones) as ydl:
        ydl.download([url])
