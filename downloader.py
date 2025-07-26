import os
import re
from yt_dlp import YoutubeDL
from utils import limpiar_ansi, get_ffmpeg_paths

def descargar_video(url: str, solo_audio: bool, destino: str, callback_progreso=None, callback_estado=None, calidad="best", formato="mp4"):

    ffmpeg_path, ffprobe_path = get_ffmpeg_paths()

    def hook(d):
        # Print status for debugging and tracking
        print(f"[yt-dlp] Status: {d.get('status')}, Progress: {d.get('_percent_str', '')}")
        if d['status'] == 'downloading' and callback_progreso:
            pct_str = d.get('_percent_str', '0%')
            pct_str = limpiar_ansi(pct_str).strip().replace('%', '').replace(',', '.')
            try:
                callback_progreso(float(pct_str))
            except ValueError:
                pass
        elif d['status'] == 'finished':
            if callback_progreso:
                callback_progreso(100)
            if callback_estado:
                callback_estado("✅ ¡Download completed!")

    # Use %(title)s.%(ext)s so yt-dlp manages extensions and overwrites properly
    opciones = {
        'format': 'bestaudio/best' if solo_audio else calidad,
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
        'progress_hooks': [hook],
        'quiet': True,
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [],
        'overwrites': True,
        'merge_output_format': None if solo_audio else formato,
        'keepvideo': False,
        'continuedl': True,
        'ignoreerrors': True,  # Continue on errors (useful for playlists)
        'yesplaylist': True,   # Always download playlist if URL is a playlist
        'noplaylist': False,   # Never disable playlist mode
    }

    if solo_audio:
        opciones['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': formato,
            'preferredquality': '192',
        })
        # Ensure only the final audio file is kept
        opciones['outtmpl'] = os.path.join(destino, '%(title)s.%(ext)s')

    try:
        with YoutubeDL(opciones) as ydl:
            print(f"[yt-dlp] Downloading: {url}")
            ydl.download([url])
    except Exception as e:
        print(f"[yt-dlp][ERROR] {e}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
            callback_estado(f"❌ Error: {str(e)}")
