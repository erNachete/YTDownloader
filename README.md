# YTDownloader

A simple YouTube video downloader with a graphical interface, built in Python using `yt-dlp` and `Tkinter`.

🎥 Perfect for users who want a GUI app with dropdowns and checkboxes — no command line needed.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![yt-dlp](https://img.shields.io/badge/backend-yt--dlp-orange)
![MIT License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-beta-yellow)

---

## 📦 Latest Version

**`v0.1 – 2025-07-25`**  
👉 [Download Windows executable (.exe)](https://github.com/erNachete/YTDownloader/releases/download/0.1/ytdwnlr.exe)

> ⚠️ Note: Some antivirus tools might flag the `.exe` as a false positive since it was built using PyInstaller. You can verify it's safe using [VirusTotal](https://www.virustotal.com/).

---

## 🖥️ Features

- ✅ Download YouTube videos with one click
- ✅ "Audio only" mode (MP3)
- ✅ Destination folder selector
- ✅ Progress bar
- ✅ "Download complete!" message
- ✅ No command line required

---

## 📷 Screenshot

![YTDownloader GUI Screenshot](docs/screenshot.png) <!-- comment if you don't have it yet -->

---

## 🧪 Run from Source (Dev Mode)

```bash
git clone https://github.com/erNachete/YTDownloader.git
cd YTDownloader
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
