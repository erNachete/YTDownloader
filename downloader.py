import os
import re
from yt_dlp import YoutubeDL

def descargar_video(url: str, solo_audio: bool, destino: str, callback_progreso=None, callback_estado=None, calidad="best", formato="mp4"):

    ffmpeg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe'))
    ffprobe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffprobe.exe'))

    def limpiar_ansi(texto):
        return re.sub(r'\x1b\[[0-9;]*m', '', texto)

    def hook(d):
        print(callback_progreso)
        print(d['status'])
        if d['status'] == 'downloading' and callback_progreso:
            pct_str = d.get('_percent_str', '0%')
            pct_str = limpiar_ansi(pct_str).strip().replace('%', '').replace(',', '.')
            print(pct_str)
            print(float(pct_str))
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
        'merge_output_format': formato if not solo_audio else None,  # Ensures final extension is correct
        'keepvideo': False,  # Remove temp files after merge/convert
    }

    if not solo_audio:
        # No need to add FFmpegVideoConvertor if using merge_output_format
        pass
    else:
        opciones['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    try:
        with YoutubeDL(opciones) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"[ERROR] {e}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        print(f"[ERROR] {e}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
        if callback_estado:
            callback_estado(f"❌ Error: {str(e)}")
