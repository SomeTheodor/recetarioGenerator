from flask import Blueprint, render_template, request, redirect, send_file, current_app, abort
from .repository import load_data, save_data, get_receta_by_id
from .services import crear_receta, generar_pdf

main = Blueprint("main", __name__)

@main.route("/")
def index():
    data = load_data(current_app.config["JSON_FILE"])
    recetas = data["recetas"]
    recetas_por_categoria = {}
    for receta in recetas:
        recetas_por_categoria.setdefault(receta["categoria"], []).append(receta)
    return render_template(
        "index.html",
        recetas_por_categoria=recetas_por_categoria)


@main.route("/crear", methods=["POST"])
def crear():
    json_path = current_app.config["JSON_FILE"]
    data = load_data(json_path)

    data = crear_receta(data, request.form)
    save_data(json_path, data)

    return redirect("/")


@main.route("/pdf/<int:receta_id>")
def pdf(receta_id):
    json_path = current_app.config["JSON_FILE"]
    data = load_data(json_path)

    receta = get_receta_by_id(data, receta_id)
    if not receta:
        abort(404)

    pdf_path = generar_pdf(
        receta,
        current_app.config["TEMPLATE_FILE"],
        current_app.config["OUTPUT_DIR"]
    )

    return send_file(pdf_path, as_attachment=True)