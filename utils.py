import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE
import json
import os

CONFIG_FILE = 'styles_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuración guardada en {CONFIG_FILE}")

def apply_styles(paragraph, text, style_name, style_type, doc):
    styles = doc.styles
    if style_name not in [style.name for style in styles]:
        if style_type == 'parrafo':
            style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        elif style_type == 'caracter':
            style = styles.add_style(style_name, WD_STYLE_TYPE.CHARACTER)
        font = style.font
        font.size = Pt(12)  # Ajusta el tamaño de fuente si es necesario

    run = paragraph.add_run(text)
    if style_type == 'parrafo':
        paragraph.style = style_name
    elif style_type == 'caracter':
        run.style = style_name

def clean_default_styles(doc):
    styles = doc.styles
    keep_styles = {s['style'] for s in load_config().values()}
    keep_styles.add("Agenda-General-Parrafo")  # Include the general paragraph style
    keep_styles.add("Agenda-General-Caracter")  # Include the general character style

    for style in list(styles):
        if style.type in (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER) and style.name not in keep_styles:
            styles.element.remove(style.element)

def process_xml_to_docx(xml_file, output_folder, output_file_name):
    config = load_config()
    tree = ET.parse(xml_file)
    root = tree.getroot()

    doc = Document()

    # Create "Agenda-General-Parrafo" and "Agenda-General-Caracter" styles
    if "Agenda-General-Parrafo" not in [style.name for style in doc.styles]:
        general_paragraph_style = doc.styles.add_style("Agenda-General-Parrafo", WD_STYLE_TYPE.PARAGRAPH)
        general_paragraph_style.font.size = Pt(12)

    if "Agenda-General-Caracter" not in [style.name for style in doc.styles]:
        general_character_style = doc.styles.add_style("Agenda-General-Caracter", WD_STYLE_TYPE.CHARACTER)
        general_character_style.font.size = Pt(12)

    def process_element(element, field, paragraph):
        if element is not None and element.text and element.text.strip():
            style_name = config.get(field, {}).get('style', "Agenda-General-Caracter" if config.get(field, {}).get('type', 'parrafo') == 'caracter' else "Agenda-General-Parrafo")
            style_type = config.get(field, {}).get('type', 'caracter')  # Default to 'caracter'
            apply_styles(paragraph, element.text, style_name, style_type, doc)

    def process_fields(parent_element, fields):
        for field in fields:
            element = parent_element.find(field)
            if element is not None and element.text and element.text.strip():
                p = doc.add_paragraph()
                process_element(element, field, p)

    for event in root.findall('Evento-Principal'):
        process_fields(event, config.keys())

        programa = event.find('Evento-Principal-Programa')
        if programa is not None:
            for sub_event in programa.findall('Sub-evento'):
                process_fields(sub_event, config.keys())

                actividades = sub_event.find('Sub-evento-actividades')
                if actividades is not None:
                    for actividad in actividades.findall('actividad'):
                        process_fields(actividad, config.keys())

    # Clean default styles
    clean_default_styles(doc)

    # Apply "Agenda-General-Parrafo" style to all paragraphs if no style is set
    for paragraph in doc.paragraphs:
        if paragraph.style is None or paragraph.style.name == 'Normal':  # Change default Normal style to Agenda-General-Parrafo
            paragraph.style = "Agenda-General-Parrafo"

    output_path = os.path.join(output_folder, output_file_name)
    doc.save(output_path)
    print(f"Document saved to {output_path}")
