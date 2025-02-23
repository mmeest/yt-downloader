import yt_dlp
import tkinter as tk
import os
import logging
import threading
from tkinter import ttk, simpledialog
from urllib.parse import urlparse, parse_qs
import re

# Konfigureeri logger
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

# Loo "downloads" kataloog
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

# URL puhastamine
def clean_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if "v" in query_params:
        return f"https://www.youtube.com/watch?v={query_params['v'][0]}"
    return url

# Faili olemasolu käsitlemine
def handle_existing_file(title, file_format):
    new_filename = title  # Algne nimi

    def on_rename():
        nonlocal new_filename
        new_filename = rename_entry.get()
        dialog.destroy()

    def on_overwrite():
        dialog.destroy()

    def on_cancel():
        nonlocal new_filename
        new_filename = None  # Katkesta allalaadimine
        dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Fail Eksisteerib")
    tk.Label(dialog, text=f"Fail '{title}.{file_format}' eksisteerib. Mida soovid teha?").pack(pady=10)

    rename_entry = tk.Entry(dialog, width=40)
    rename_entry.insert(0, title)
    rename_entry.pack(pady=5)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Nimeta ümber", command=on_rename).pack(side="left", padx=5)
    tk.Button(button_frame, text="Kirjuta üle", command=on_overwrite).pack(side="left", padx=5)
    tk.Button(button_frame, text="Tühista allalaadimine", command=on_cancel).pack(side="left", padx=5)

    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

    return new_filename

# Faili nime kontroll
def get_unique_filename(url, file_format):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'unknown')
    
    file_path = os.path.join(download_dir, f"{title}.{file_format}")
    if os.path.exists(file_path):
        new_title = handle_existing_file(title, file_format)
        if new_title is None:
            return None  # Kui kasutaja katkestab, lõpetame
        return os.path.join(download_dir, f"{new_title}.{file_format}")  

    return file_path

# Progressi uuendamine
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

# Video allalaadimine
def download_video():
    url = url_entry.get().strip()
    if not url:
        status_label.config(text="Palun sisesta Youtube URL!", fg="red")
        return

    url = clean_url(url)
    resolution = resolution_var.get()

    # Kontrollime faili olemasolu ENNE progressbari käivitamist
    file_format = "mp4" if resolution != "MP3 (audio only)" else "mp3"
    output_filename = get_unique_filename(url, file_format)

    if output_filename is None:
        status_label.config(text="Allalaadimine katkestatud.", fg="red")
        return

    # Kui kasutaja ei katkestanud, alles siis käivitame progressbari
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
            progress_bar.stop()  # Peatame progressbari igal juhul

    threading.Thread(target=run_download, daemon=True).start()

# Paremkliki "paste" funktsioon
def paste_from_clipboard(event):
    url_entry.delete(0, tk.END)
    url_entry.insert(0, root.clipboard_get())

# GUI seaded
root = tk.Tk()
root.title("Youtube Video Allalaadija")
root.geometry("400x280")

# URL sisestus
tk.Label(root, text="Sisesta Youtube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.bind("<Button-3>", paste_from_clipboard)  # Paremkliki tugi

# Resolutsiooni valik
tk.Label(root, text="Vali resolutsioon:").pack(pady=5)
resolution_var = tk.StringVar(root)
resolution_var.set('best')
resolutions = ['best', '720p', '1080p', '1440p', '2160p', 'worst', 'MP3 (audio only)']
resolution_menu = tk.OptionMenu(root, resolution_var, *resolutions)
resolution_menu.pack(pady=5)

# Progressbar
progress_bar = ttk.Progressbar(root, length=200, mode="determinate")
progress_bar.pack(pady=10)

# Staatus
status_label = tk.Label(root, text="", fg="black")
status_label.pack(padx=5)

# Allalaadimise nupp
tk.Button(root, text="Laadi alla", command=download_video).pack(pady=10)

# Käivita GUI
root.mainloop()
