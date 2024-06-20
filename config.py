import tkinter as tk
from tkinter import messagebox
import json
import os

CONFIG_FILE = 'styles_config.json'

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuración guardada en {CONFIG_FILE}")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

def start_config_gui():
    def update_config():
        config = {}
        for field, style_var in fields.items():
            config[field] = {'type': 'caracter', 'style': style_var.get()}
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
        
        style_var = tk.StringVar(value=config.get(field, {}).get('style', field))  # Default style name to field name

        tk.Entry(root, textvariable=style_var).grid(row=idx, column=1, padx=10, pady=5)

        fields[field] = style_var

    tk.Button(root, text="Guardar Configuración", command=update_config).grid(row=len(xml_structure), column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_config_gui()
