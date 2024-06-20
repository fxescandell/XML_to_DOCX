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

def apply_styles(paragraph, text, style_name, doc):
    styles = doc.styles
    if style_name not in [style.name for style in styles]:
        style = styles.add_style(style_name, WD_STYLE_TYPE.CHARACTER)
        font = style.font
        font.size = Pt(12)  # Ajusta el tamaño de fuente si es necesario

    run = paragraph.add_run(text)
    run.style = style_name

def process_xml_to_docx(xml_file, output_folder, output_file_name):
    config = load_config()
    tree = ET.parse(xml_file)
    root = tree.getroot()

    doc = Document()

    def process_element(element, field):
        if element is not None and element.text:
            p = doc.add_paragraph()
            style_name = config.get(field, {}).get('style', field)  # Use default style name if not found
            apply_styles(p, element.text, style_name, doc)

    for event in root.findall('Evento-Principal'):
        for field in config.keys():
            process_element(event.find(field), field)

        programa = event.find('Evento-Principal-Programa')
        if programa is not None:
            for sub_event in programa.findall('Sub-evento'):
                for field in config.keys():
                    process_element(sub_event.find(field), field)

                actividades = sub_event.find('Sub-evento-actividades')
                if actividades is not None:
                    for actividad in actividades.findall('actividad'):
                        for field in config.keys():
                            process_element(actividad.find(field), field)

    output_path = os.path.join(output_folder, output_file_name)
    doc.save(output_path)
    print(f"Document saved to {output_path}")
