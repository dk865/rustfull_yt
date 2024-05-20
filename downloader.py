import tkinter as tk
from tkinter import ttk
import threading
import os
import sys
import yt_dlp
import certifi

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def start_download():
    url = url_entry.get()
    format_selected = format_combo.get()
    url_entry.config(state=tk.DISABLED)
    format_combo.config(state=tk.DISABLED)
    start_button.config(state=tk.DISABLED)
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Warming up, please wait!\n")
    output_text.config(state=tk.DISABLED)
    thread = threading.Thread(target=run_command, args=(url, format_selected))
    thread.start()

def run_command(url, format_selected):
    ydl_opts = {
        'format': format_selected,
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'nocheckcertificate': True,
        'ca_certs': certifi.where(),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"Error: {str(e)}\n")
            output_text.config(state=tk.DISABLED)

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "\nDownload Complete!\nThe file has been placed in the current directory.")
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)
    url_entry.config(state=tk.NORMAL)
    format_combo.config(state=tk.NORMAL)
    start_button.config(state=tk.NORMAL)

def progress_hook(d):
    if d['status'] == 'downloading':
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, f"\r{d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA {d['_eta_str']}\n")
        output_text.see(tk.END)
        output_text.config(state=tk.DISABLED)

def check_input(event=None):
    if url_entry.get() and format_combo.get():
        start_button.config(state=tk.NORMAL)
    else:
        start_button.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Rustful Youtube Downloader")
root.iconbitmap(resource_path("icon.ico"))

# Title label
title_label = tk.Label(root, text="Rustful Youtube Downloader", font=("Helvetica", 16))
title_label.pack(pady=10)

# Subtitle label
subtitle_label = tk.Label(root, text="Made by dk865", font=("Helvetica", 12))
subtitle_label.pack(pady=(0, 20))

# URL input
url_label = tk.Label(root, text="Youtube URL")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()
url_entry.bind("<KeyRelease>", check_input)

# Download format dropdown
format_label = tk.Label(root, text="Download Format")
format_label.pack()
format_combo = ttk.Combobox(root, values=["m4a", "mp4"], width=47, state="readonly")
format_combo.pack()
format_combo.bind("<<ComboboxSelected>>", check_input)

# Start button
start_button = tk.Button(root, text="Start!", command=start_download, state=tk.DISABLED)
start_button.pack(pady=20)

# Output text box
output_text = tk.Text(root, height=10, width=60)
output_text.pack()

# Run the application
root.mainloop()
