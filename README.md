# YTDownloader 

A simple YouTube video downloader with a graphical interface, built in Python using `yt-dlp` and `Tkinter`.

---

## What can YTDownloader do?

- **Download individual YouTube videos**: Paste any YouTube video URL and download it directly.
- **Download entire playlists**: Paste a playlist URL and the app will automatically download all videos in the list.
- **Select video quality**: Choose the quality of the video you want to download (from 4K to 360p).
- **Select output format**: Download videos in your preferred format (mp4, avi, mkv, webm).
- **Audio only mode**: Download just the audio from a video or playlist, and choose the audio format (mp3, aac, wav, m4a, opus).
- **Choose destination folder**: Save your downloads wherever you want.
- **See download progress**: Visual progress bar and a list showing the status (pending, downloading, completed, error) for each video.
- **Resume interrupted downloads**: If a download is interrupted, it will continue from where it left off.
- **Automatic conversion**: The app uses ffmpeg to ensure your downloads are in the format you selected.
- **No command line needed**: Everything is managed from a simple graphical interface.

---

## 📦 Latest Version

**`v0.2 – 2025-07-26`**  
👉 [Download Windows executable (.exe)](https://github.com/erNachete/YTDownloader/releases/download/0.2/ytdwnlr.exe)

### What's new in v0.2

- Playlist support: paste a playlist URL and download all videos automatically.
- Download list: see the status (pending, downloading, completed, error) for each video in the playlist or batch.
- Improved progress and status reporting.
- File existence check: warns if a file already exists before downloading (for single videos).
- Improved icon handling and packaging for both the GUI and the executable.
- The app window is now always centered on the screen.
- Keeps only the final file (no temp/intermediate files).
- Resumes interrupted downloads automatically.
- ffmpeg and ffprobe are bundled for conversion and merging.

---

**`v0.1 – 2025-07-25`**  
👉 [Download Windows executable (.exe)](https://github.com/erNachete/YTDownloader/releases/download/0.1/ytdwnlr.exe)

> ⚠️ Note: Some antivirus tools might flag the `.exe` as a false positive since it was built using PyInstaller. You can verify it's safe using [VirusTotal](https://www.virustotal.com/).

---

## 📷 Screenshot

![YTDownloader GUI Screenshot](docs/screenshot.png) <!-- comment if you don't have it yet -->

---

## How to use

1. Paste a YouTube video or playlist URL.
2. (Optional) Select "Audio only" if you want just the audio.
3. Choose the desired video or audio format.
4. Select the destination folder.
5. Click "Download".
6. Watch the progress and status for each item in the list.

---

## Requirements

- Windows (for the .exe)
- Python 3.11+ (if running from source)
- yt-dlp, tkinter, Pillow (see requirements.txt)
- ffmpeg and ffprobe (included in the build for Windows)

---

## Build instructions

See the section "Build Windows Executable" in this README for details on how to build your own `.exe` with all dependencies included.

---

## 📁 Project Structure

```
ytdwnlr/
├── build_exe.py
├── downloader.py
├── gui.py
├── main.py
├── requirements.txt
├── ffmpeg/
│   ├── ffmpeg.exe
│   └── ffprobe.exe
├── icon.ico
├── README.md
└── .gitignore
```

---

## ⚙️ Requirements

- Python 3.11+ (recommended)
- yt-dlp
- tkinter (comes with Python)
- Pillow (for icon support, optional)
- ffmpeg and ffprobe (included in the build for Windows)

---

## 📝 Notes

- The app supports both single video and playlist URLs. For playlists, all items are downloaded and shown in the download list.
- The download list shows the status of each video: pending, downloading, completed, or error.
- If you select "Audio only", you can choose the output audio format.
- If you select video, you can choose the output video format.
- The app checks if the output file already exists (for single videos) and warns you before downloading.
- All downloads use ffmpeg for conversion and merging, and only the final file is kept.
- The app resumes interrupted downloads automatically.
- The build script (`build_exe.py`) ensures all resources are included for the standalone executable.

---

## 🚫 .gitignore

Make sure your `.gitignore` includes:
```
icon.ico
dist/
build/
__pycache__/
*.spec
venv/
```

---

## 💡 Troubleshooting

- If the icon does not appear in the exe, ensure `icon.ico` exists before building and that you are running the exe from the `dist/` folder.
- If ffmpeg is not found, make sure the `ffmpeg` folder is present in your project root before building.
- If you get errors about missing modules, check that all requirements are installed in your virtual environment.

---
icon.ico
dist/
build/
__pycache__/
*.spec
venv/
```

---

## 💡 Troubleshooting

- If the icon does not appear in the exe, ensure `icon.ico` exists before building and that you are running the exe from the `dist/` folder.
- If ffmpeg is not found, make sure the `ffmpeg` folder is present in your project root before building.
- If you get errors about missing modules, check that all requirements are installed in your virtual environment.

---

## 💡 Troubleshooting

- If the icon does not appear in the exe, ensure `icon.ico` exists before building and that you are running the exe from the `dist/` folder.
- If ffmpeg is not found, make sure the `ffmpeg` folder is present in your project root before building.
- If you get errors about missing modules, check that all requirements are installed in your virtual environment.

---
- If you get errors about missing modules, check that all requirements are installed in your virtual environment.

---
