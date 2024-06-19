# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import threading
import json
from utils import process_xml_to_docx

def start_gui():
    def select_xml_file():
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        xml_file_var.set(file_path)

    def select_output_folder():
        folder_path = filedialog.askdirectory()
        output_folder_var.set(folder_path)

    def start_processing():
        threading.Thread(target=process_file).start()

    def process_file():
        xml_file = xml_file_var.get()
        output_folder = output_folder_var.get()
        if not xml_file or not output_folder:
            messagebox.showerror("Error", "Por favor, selecciona un archivo XML y una carpeta de salida.")
            return

        progress_var.set(0)
        status_var.set("Procesando...")
        process_xml_to_docx(xml_file, output_folder, update_progress)
        status_var.set("Completado")

    def update_progress(value):
        progress_var.set(value)

    root = tk.Tk()
    root.title("XML to DOCX Converter")

    xml_file_var = tk.StringVar()
    output_folder_var = tk.StringVar()
    progress_var = tk.IntVar()
    status_var = tk.StringVar()

    tk.Label(root, text="Seleccionar archivo XML:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=xml_file_var, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_xml_file).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Seleccionar carpeta de salida:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(root, text="Iniciar Proceso", command=start_processing).grid(row=2, column=1, pady=10)

    progress = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate', variable=progress_var)
    progress.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, textvariable=status_var).grid(row=4, column=1, padx=10, pady=10)

    root.mainloop()
