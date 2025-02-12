import yt_dlp
import tkinter as tk
# from tkinter import messagebox # deprecated
import os   # for download folder
import logging
import threading
from tkinter import ttk, simpledialog
from urllib.parse import urlparse, parse_qs
import re


def start_download():
    threading.Thread(target=run_download, daemon=True).start()

# Configurating logger
def configure_logger():
    logger = logging.getLogger("yt-dlp")
    if not logger.handlers:  # Kontrollib, kas logimisandurid on juba lisatud
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)  # Set log level to DEBUG
    # handler = logging.StreamHandler()  # Log to console
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    return logger

# Logger
logger = configure_logger()

# Creates downloads folder
download_dir = os.path.join(os.getcwd(), "downloads")  # Loob "downloads" kausta
os.makedirs(download_dir, exist_ok=True)

# To remove 'list' from YouTube video url
def clean_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if "v" in query_params:
        # video_id = query_params["v"][0]
        # return f"https://www.youtube.com/watch?v={video_id}"
        return f"https://www.youtube.com/watch?v={query_params['v'][0]}"
    return url

def download_video():
    #   url = clean_url(url_entry.get())
    url = url_entry.get().strip()
    if not url:
        # messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        status_label.config(text="Please enter a valid Youtube URL!", fg="red")
        return
    
    url = clean_url(url)
    resolution = resolution_var.get()
    
    status_label.config(text="Downloading...", fg="blue")
    progress_bar.start()

    # Defining different resolutions
    resolution_map = {
        'best': 'bestvideo+bestaudio/best',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        'worst': 'worstvideo+bestaudio',
        'MP3 (audio only)': 'bestaudio/best'
    }

    # File output format
    file_format = "mp4" if resolution != "MP3 (audio only)" else "mp3"
    
    # Generate output file path
    output_filename = os.path.join(download_dir, "%(title)s.%(ext)s")

    # Check if file exists and ask for rename
    def get_unique_filename():
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'unknown')
        
        file_path = os.path.join(download_dir, f"{title}.{file_format}")
        if os.path.exists(file_path):
            new_title = simpledialog.askstring("File Exists", f"File '{title}.{file_format}' exists. Enter new name:", initialvalue=title)
            if new_title:
                return os.path.join(download_dir, f"{new_title}.{file_format}")
        return file_path

    output_filename = get_unique_filename()
    
    # YT-DLP configuration
    ydl_opts = {
        # 'format': resolution, # Selected resolution - deprecated
        'format': resolution_map.get(resolution, 'best'),  # Using resolution map
        'merge_output_format': 'mp4',
        # 'outtmpl': '%(title)s.%(ext)s',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': False,  # Disable quiet mode to see logs
        'logger': logger,
        'verbose': True  # Enable verbose mode for more detailed logs
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
    # run_download()
    threading.Thread(target=run_download, daemon=True).start()

def progress_hook(d):
    if d['status'] == 'downloading':
        # We'll remove color codes using RegEx
        """
        progress = d.get('_percent_str', "0%").strip('%')
        progress = re.sub(r'\x1b\[[0-9;]*m', '', progress)  # Removes color codes
        if progress:
            try:
                progress_bar["value"] = float(progress)
                status_label.config(text=f"Downloading: {progress}%")
            except ValueError:
                # If conversion fails - we continue progress update
                pass
        """
        progress = d.get('_percent_str', "0%").strip('%').strip()
        progress = re.sub(r'\x1b\[[0-9;]*m', '', progress)  # Remove ANSI color codes
        if progress.isdigit():
            progress_bar["value"] = float(progress)
            status_label.config(text=f"Downloading: {progress}%")
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