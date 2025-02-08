import yt_dlp
import tkinter as tk
# from tkinter import messagebox # deprecated
import logging
from tkinter import ttk
from urllib.parse import urlparse, parse_qs

# Configurating logger
def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set log level to DEBUG
    handler = logging.StreamHandler()  # Log to console
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Logger
logger = configure_logger()

# To remove 'list' from YouTube video url
def clean_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if "v" in query_params:
        video_id = query_params["v"][0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def download_video():
    url = clean_url(url_entry.get())
    resolution = resolution_var.get()

    if not url:
        # messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        status_label.config(text="Please enter a valid Youtube URL!", fg="red")
        return
    
    status_label.config(text="Downloading...", fg="blue")
    progress_bar.start()

    # Defining different resolutions
    resolution_map = {
        'best': 'bestvideo+bestaudio/best',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        'worst': 'worstvideo+bestaudio'
    }
    
    # YT-DLP configuration
    ydl_opts = {
        # 'format': resolution, # Selected resolution - deprecated
        'format': resolution_map.get(resolution, 'best'),  # Using resolution map
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': False,  # Disable quiet mode to see logs
        'logger': logger,
        'verbose': True  # Enable verbose mode for more detailed logs
    }

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url]) # Downloads video
            # messagebox.showinfo("Success", "Download completed successfully!") # depcrecated message box
            status_label.config(text="Download complete!", fg="green")
        except Exception as e:
            # messagebox.showerror("Error", f"Error downloading video: {str(e)}") # deprecated
            status_label.config(text=f"Error: {str(e)}", fg="red")
        finally:
            progress_bar.stop()

    # Download process starts in background, for not to disturb GUI
    # root.after(100, run_download)
    run_download()

import re

def progress_hook(d):
    if d['status'] == 'downloading':
        # We'll remove color codes using RegEx
        progress = d.get('_percent_str', "0%").strip('%')
        progress = re.sub(r'\x1b\[[0-9;]*m', '', progress)  # Removes color codes
        if progress:
            try:
                progress_bar["value"] = float(progress)
                status_label.config(text=f"Downloading: {progress}%")
            except ValueError:
                # If conversion fails - we continue progress update
                pass
    elif d['status'] == 'finished':
        status_label.config(text="Download complete!", fg="green")
        progress_bar["value"] = 100



# Generating window
root = tk.Tk()
root.title("Youtube Video Downloader")
root.geometry("400x250")

# Field for inserting URL
url_label = tk.Label(root, text="Enter Youtube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Resolution selection
resolution_label = tk.Label(root, text="Select Resolution:")
resolution_label.pack(pady=5)
resolution_var = tk.StringVar(root)
resolution_var.set('best')  # Best resolution by default
resolutions= ['best', '720p', '1080p', '1440p', '2160p', 'worst']
resolution_menu = tk.OptionMenu(root, resolution_var, *resolutions)
resolution_menu.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, length=200, mode="determinate")
progress_bar.pack(pady=10)

# Status message
status_label = tk.Label(root, text="", fg="black")
status_label.pack(padx=5)

# Download button
download_button = tk.Button(root, text="Download Video", command=download_video)
download_button.pack(pady=10)

# Starting application
root.mainloop()