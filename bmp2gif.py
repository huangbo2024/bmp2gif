'''
在我做项目时，一个小工作是把material studio导出的很多bmp图片连续拼接成gif，所以编写了此脚本自动拼接
When I was working on the project, a small task was to continuously splice a lot of .bmp images exported by material studio into .gif, 
so I wrote this script for automatic stitching.
'''
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import threading


class BMP2GIFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMP to GIF Converter")

        # Create and set the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="BMP Folder Path:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(self.root, text="Output GIF Path:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(self.root, text="Frame Duration (ms):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry widgets to display selected paths
        self.bmp_dir_entry = tk.Entry(self.root, width=50)
        self.bmp_dir_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.gif_output_entry = tk.Entry(self.root, width=50)
        self.gif_output_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.frame_duration_entry = tk.Entry(self.root, width=10)
        self.frame_duration_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        self.frame_duration_entry.insert(0, "200")  # Default value

        # Buttons to open file dialogs
        tk.Button(self.root, text="Browse", command=self.browse_bmp).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Save As", command=self.browse_gif).grid(row=1, column=2, padx=10, pady=10)

        # Convert Button
        tk.Button(self.root, text="Convert to GIF", command=self.convert_to_gif).grid(row=3, column=0, columnspan=3,
                                                                                      pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

    def browse_bmp(self):
        folder_path = filedialog.askdirectory(title="Select BMP Folder")
        if folder_path:
            self.bmp_dir_entry.delete(0, tk.END)
            self.bmp_dir_entry.insert(0, folder_path)

    def browse_gif(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if file_path:
            self.gif_output_entry.delete(0, tk.END)
            self.gif_output_entry.insert(0, file_path)

    def bmp_to_gif(self, bmp_dir, output_gif, duration):
        bmp_files = [f for f in os.listdir(bmp_dir) if f.endswith('.bmp') or f.endswith('.BMP')]
        bmp_files.sort()
        images = [Image.open(os.path.join(bmp_dir, f)) for f in bmp_files]
        images[0].save(output_gif, save_all=True, append_images=images[1:], loop=0, duration=duration)
        self.progress['value'] = 100
        self.root.after(0, lambda: messagebox.showinfo("Info", "Conversion completed!"))

    def convert_to_gif(self):
        bmp_dir = self.bmp_dir_entry.get()
        output_gif = self.gif_output_entry.get()
        try:
            duration = int(self.frame_duration_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please provide a valid frame duration!")
            return

        if not bmp_dir or not output_gif:
            return

        self.progress['value'] = 0
        thread = threading.Thread(target=self.bmp_to_gif, args=(bmp_dir, output_gif, duration))
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMP2GIFApp(root)
    root.mainloop()
