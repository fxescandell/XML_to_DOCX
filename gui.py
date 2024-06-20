import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import json
import os
import subprocess
import platform
from utils import process_xml_to_docx, load_config, save_config

CONFIG_FILE = 'styles_config.json'

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

    def open_styles_config():
        config_file_path = CONFIG_FILE
        if not os.path.exists(config_file_path):
            messagebox.showerror("Error", f"El archivo {config_file_path} no existe.")
            return

        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', config_file_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(config_file_path)
            else:  # Linux variants
                subprocess.call(('xdg-open', config_file_path))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def update_config():
        config = {}
        for field, (type_var, style_var) in fields.items():
            config[field] = {'type': type_var.get(), 'style': style_var.get()}
        save_config(config)
        messagebox.showinfo("Información", "Configuración guardada correctamente.")

    root = tk.Tk()
    root.title("XML to DOCX Converter")

    xml_file_var = tk.StringVar()
    output_folder_var = tk.StringVar()
    output_file_var = tk.StringVar()
    status_var = tk.StringVar()

    config = load_config()

    fields = {}

    xml_structure = [
        'Evento-Principal-Titulo',
        'Evento-Principal-Dia',
        'Evento-Principal-Hora',
        'Evento-Principal-Lugar',
        'Evento-Principal-Descripcion',
        'Sub-evento-Titulo',
        'Sub-evento-Dia',
        'Sub-evento-Hora',
        'Sub-evento-Lugar',
        'Sub-evento-descripcion',
        'actividad-titulo',
        'actividad-hora',
        'actividad-lugar',
        'actividad-descipción'
    ]

    # Left column for XML fields and style settings
    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')

    tk.Label(left_frame, text="Campos del XML y Estilos").grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    for idx, field in enumerate(xml_structure):
        tk.Label(left_frame, text=field).grid(row=idx + 1, column=0, padx=10, pady=5)
        
        type_var = tk.StringVar(value=config.get(field, {}).get('type', 'caracter'))
        style_var = tk.StringVar(value=config.get(field, {}).get('style', field))  # Default style name to field name

        tk.Radiobutton(left_frame, text="Párrafo", variable=type_var, value='parrafo').grid(row=idx + 1, column=1, padx=5)
        tk.Radiobutton(left_frame, text="Carácter", variable=type_var, value='caracter').grid(row=idx + 1, column=2, padx=5)
        tk.Entry(left_frame, textvariable=style_var).grid(row=idx + 1, column=3, padx=10, pady=5)

        fields[field] = (type_var, style_var)

    # Right column for file selection and processing buttons
    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

    tk.Label(right_frame, text="Seleccionar archivo XML:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(right_frame, textvariable=xml_file_var, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(right_frame, text="Browse", command=select_xml_file).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(right_frame, text="Seleccionar carpeta de salida:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(right_frame, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(right_frame, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

    tk.Label(right_frame, text="Nombre del archivo de salida:").grid(row=2, column=0, padx=10, pady=10)
    tk.Entry(right_frame, textvariable=output_file_var, width=50).grid(row=2, column=1, padx=10, pady=10)

    tk.Button(right_frame, text="Iniciar Proceso", command=start_processing).grid(row=3, column=1, pady=10)
    tk.Button(right_frame, text="Ver Configuración de Estilos", command=open_styles_config).grid(row=4, column=1, pady=10)
    tk.Button(right_frame, text="Guardar Configuración de Estilos", command=update_config).grid(row=5, column=1, pady=10)

    tk.Label(right_frame, textvariable=status_var).grid(row=6, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
