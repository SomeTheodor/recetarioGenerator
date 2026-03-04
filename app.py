from flask import Flask, render_template, request, redirect, send_file
import json
import os
from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "data.json")
TEMPLATE_FILE = os.path.join(BASE_DIR, "template.docx")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar recetas
def load_data():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    data = load_data()
    return render_template("form.html", recetas=data["recetas"])


@app.route("/crear", methods=["POST"])
def crear_receta():
    data = load_data()

    nueva_receta = {
        "id": len(data["recetas"]) + 1,
        "nombre": request.form["nombre"],
        "categoria": request.form["categoria"],
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "ingredientes": request.form["ingredientes"].split("\n"),
        "pasos": request.form["pasos"].split("\n")
    }

    data["recetas"].append(nueva_receta)
    save_data(data)

    return redirect("/")


@app.route("/pdf/<int:receta_id>")
def generar_pdf(receta_id):
    data = load_data()
    receta = next((r for r in data["recetas"] if r["id"] == receta_id), None)

    if not receta:
        return "Receta no encontrada"

    doc = DocxTemplate(TEMPLATE_FILE)
    doc.render(receta)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    docx_path = os.path.join(OUTPUT_DIR, f"receta_{timestamp}.docx")
    pdf_path = os.path.join(OUTPUT_DIR, f"receta_{timestamp}.pdf")

    doc.save(docx_path)
    convert(docx_path, pdf_path)
    os.remove(docx_path)

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)