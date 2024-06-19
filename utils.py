# utils.py

import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Pt
import json

CONFIG_FILE = 'styles_config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def apply_styles(paragraph, text, style_type, style_name):
    run = paragraph.add_run(text)
    if style_type == 'parrafo':
        paragraph.style = style_name
    elif style_type == 'caracter':
        run.style = style_name
    run.font.size = Pt(12)  # Ajusta el tamaño de fuente si es necesario

def process_xml_to_docx(xml_file, output_folder, update_progress):
    config = load_config()
    tree = ET.parse(xml_file)
    root = tree.getroot()

    doc = Document()
    total_elements = len(root.findall('.//*'))
    processed_elements = 0

    def update_progress_inner():
        nonlocal processed_elements
        processed_elements += 1
        progress = int((processed_elements / total_elements) * 100)
        update_progress(progress)

    for event in root.findall('Evento-Principal'):
        for field, style in config.items():
            element = event.find(field)
            if element is not None and element.text:
                p = doc.add_paragraph()
                apply_styles(p, element.text, style['type'], style['style'])
                update_progress_inner()

        for sub_event in event.find('Evento-Principal-Programa').findall('Sub-evento'):
            for field, style in config.items():
                element = sub_event.find(field)
                if element is not None and element.text:
                    p = doc.add_paragraph()
                    apply_styles(p, element.text, style['type'], style['style'])
                    update_progress_inner()

            for activity in sub_event.find('Sub-evento-actividades').findall('actividad'):
                for field, style in config.items():
                    element = activity.find(field)
                    if element is not None and element.text:
                        p = doc.add_paragraph()
                        apply_styles(p, element.text, style['type'], style['style'])
                        update_progress_inner()

    doc.save(f"{output_folder}/output.docx")
