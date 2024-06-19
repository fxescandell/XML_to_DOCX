# config.py

import tkinter as tk
from tkinter import ttk, messagebox
import json

CONFIG_FILE = 'styles_config.json'

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def start_config_gui():
    def update_config():
        config = load_config()
        for field, (type_var, style_var) in fields.items():
            config[field] = {'type': type_var.get(), 'style': style_var.get()}
        save_config(config)
        messagebox.showinfo("Información", "Configuración guardada correctamente.")

    config = load_config()

    root = tk.Tk()
    root.title("Configuración de Estilos")

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

    for idx, field in enumerate(xml_structure):
        tk.Label(root, text=field).grid(row=idx, column=0, padx=10, pady=5)
        
        type_var = tk.StringVar(value=config.get(field, {}).get('type', 'parrafo'))
        tk.Radiobutton(root, text="Párrafo", variable=type_var, value='parrafo').grid(row=idx, column=1, padx=5)
        tk.Radiobutton(root, text="Carácter", variable=type_var, value='caracter').grid(row=idx, column=2, padx=5)
        
        style_var = tk.StringVar(value=config.get(field, {}).get('style', ''))
        tk.Entry(root, textvariable=style_var).grid(row=idx, column=3, padx=10, pady=5)
        
        fields[field] = (type_var, style_var)

    tk.Button(root, text="Guardar Configuración", command=update_config).grid(row=len(xml_structure), column=1, columnspan=2, pady=10)

    root.mainloop()
