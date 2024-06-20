import tkinter as tk
from tkinter import filedialog, messagebox
import threading
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
        output_file_name = output_file_var.get()
        if not xml_file or not output_folder or not output_file_name:
            messagebox.showerror("Error", "Por favor, selecciona un archivo XML, una carpeta de salida y un nombre para el archivo de salida.")
            return

        if not output_file_name.endswith(".docx"):
            output_file_name += ".docx"

        status_var.set("Procesando...")
        process_xml_to_docx(xml_file, output_folder, output_file_name)
        status_var.set("Completado")

    root = tk.Tk()
    root.title("XML to DOCX Converter")

    xml_file_var = tk.StringVar()
    output_folder_var = tk.StringVar()
    output_file_var = tk.StringVar()
    status_var = tk.StringVar()

    tk.Label(root, text="Seleccionar archivo XML:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=xml_file_var, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_xml_file).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Seleccionar carpeta de salida:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

    tk.Label(root, text="Nombre del archivo de salida:").grid(row=2, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=output_file_var, width=50).grid(row=2, column=1, padx=10, pady=10)

    tk.Button(root, text="Iniciar Proceso", command=start_processing).grid(row=3, column=1, pady=10)

    tk.Label(root, textvariable=status_var).grid(row=4, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
