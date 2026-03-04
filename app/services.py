from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
import os
import uuid

def crear_receta(data, form_data):
    nueva_receta = {
        "id": len(data["recetas"]) + 1,
        "nombre": form_data["nombre"],
        "categoria": form_data["categoria"],
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "ingredientes": form_data["ingredientes"].split("\n"),
        "pasos": form_data["pasos"].split("\n")
    }

    data["recetas"].append(nueva_receta)
    return data


def generar_pdf(receta, template_path, output_dir):
    doc = DocxTemplate(template_path)
    doc.render(receta)

    filename = f"{uuid.uuid4()}"
    docx_path = os.path.join(output_dir, f"{filename}.docx")
    pdf_path = os.path.join(output_dir, f"{filename}.pdf")

    doc.save(docx_path)
    convert(docx_path, pdf_path)
    os.remove(docx_path)

    return pdf_path