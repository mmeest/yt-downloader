import yt_dlp
import tkinter as tk
import os
import logging
import threading
from tkinter import ttk, simpledialog
from urllib.parse import urlparse, parse_qs
import re

# Configure logger
def configure_logger():
    logger = logging.getLogger("yt-dlp")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = configure_logger()

# Create "Download" folder
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

# URL cleaning
def clean_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if "v" in query_params:
        return f"https://www.youtube.com/watch?v={query_params['v'][0]}"
    return url

# Check file name for overwriting
def get_unique_filename(url, file_format):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'unknown')

    file_path = os.path.join(download_dir, f"{title}.{file_format}")
    if os.path.exists(file_path):
        new_title = simpledialog.askstring("Fail Eksisteerib", f"Fail '{title}.{file_format}' eksisteerib. Sisesta uus nimi:", initialvalue=title)
        if new_title:
            return os.path.join(download_dir, f"{new_title}.{file_format}")
    return file_path

# Progress update
def progress_hook(d):
    if d['status'] == 'downloading':
        progress = d.get('_percent_str', "0%").strip('%').strip()
        progress = re.sub(r'\x1b\[[0-9;]*m', '', progress)  # Eemaldame ANSI värvikoodid
        if progress.isdigit():
            progress_bar["value"] = float(progress)
            status_label.config(text=f"Allalaadimine: {progress}%")
    elif d['status'] == 'finished':
        status_label.config(text="Allalaadimine lõpetatud!", fg="green")
        progress_bar["value"] = 100

# Video download
def download_video():
    url = url_entry.get().strip()
    if not url:
        status_label.config(text="Palun sisesta Youtube URL!", fg="red")
        return

    url = clean_url(url)
    resolution = resolution_var.get()

    status_label.config(text="Allalaadimine...", fg="blue")
    progress_bar.start()

    resolution_map = {
        'best': 'bestvideo+bestaudio/best',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        'worst': 'worstvideo+bestaudio',
        'MP3 (audio only)': 'bestaudio/best'
    }

    file_format = "mp4" if resolution != "MP3 (audio only)" else "mp3"
    output_filename = get_unique_filename(url, file_format)

    ydl_opts = {
        'format': resolution_map.get(resolution, 'best'),
        'merge_output_format': 'mp4',
        'outtmpl': output_filename,
        'progress_hooks': [progress_hook],
        'logger': logger,
        'quiet': False,
        'verbose': True
    }

    if resolution == "MP3 (audio only)":
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'merge_output_format': 'mp3'
        })

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_label.config(text="Allalaadimine lõpetatud!", fg="green")
        except Exception as e:
            status_label.config(text=f"Viga: {str(e)}", fg="red")
        finally:
            progress_bar.stop()

    threading.Thread(target=run_download, daemon=True).start()

# Mouse right-click 'paste' function
def paste_from_clipboard(event):
    url_entry.event_generate("<<Paste>>")

# Generating GUI 
root = tk.Tk()
root.title("Youtube Video Allalaadija")
root.geometry("400x280")

# URL input
tk.Label(root, text="Sisesta Youtube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.bind("<Button-3>", paste_from_clipboard)  # Paremkliki tugi

# Resolution
tk.Label(root, text="Vali resolutsioon:").pack(pady=5)
resolution_var = tk.StringVar(root)
resolution_var.set('best')
resolutions = ['best', '720p', '1080p', '1440p', '2160p', 'worst', 'MP3 (audio only)']
resolution_menu = tk.OptionMenu(root, resolution_var, *resolutions)
resolution_menu.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, length=200, mode="determinate")
progress_bar.pack(pady=10)

# Status
status_label = tk.Label(root, text="", fg="black")
status_label.pack(padx=5)

# Download button
tk.Button(root, text="Laadi alla", command=download_video).pack(pady=10)

# Start GUI
root.mainloop()
