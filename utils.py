import os
import sys
import re

def limpiar_ansi(texto):
    """Remove ANSI escape sequences from text."""
    return re.sub(r'\x1b\[[0-9;]*m', '', texto)

def get_ffmpeg_paths():
    """Return absolute paths to ffmpeg and ffprobe executables."""
    base = os.path.abspath(os.path.dirname(__file__))
    ffmpeg_path = os.path.join(base, 'ffmpeg', 'ffmpeg.exe')
    ffprobe_path = os.path.join(base, 'ffmpeg', 'ffprobe.exe')
    return ffmpeg_path, ffprobe_path

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    Looks in current dir and in _MEIPASS if frozen.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)
