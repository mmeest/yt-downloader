import yt_dlp
import tkinter as tk
from tkinter import messagebox

def download_video():
    url = url_entry.get()
    resolution = resolution_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return
    
    # YT-DLP configuration
    ydl_opts = {
        'format': resolution, # Selected resolution
        'ottmpl': '%(title)s.%(ext)s', # Naming file according to video
        'quiet': False # Shows the process
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url]) # Downloads video
        messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading video: {str(e)}")

# Generating window
root = tk.Tk()
root.title("Youtube Video Downloader")
root.geometry("400x200")

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

# Download button
download_button = tk.Button(root, text="Download Video", command=download_video)
download_button.pack(pady=20)

# Starting application
root.mainloop()