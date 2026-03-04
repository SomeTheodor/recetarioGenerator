from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.config["BASE_DIR"] = base_dir
    app.config["JSON_FILE"] = os.path.join(base_dir, "data.json")
    app.config["TEMPLATE_FILE"] = os.path.join(base_dir, "template.docx")
    app.config["OUTPUT_DIR"] = os.path.join(base_dir, "output")

    os.makedirs(app.config["OUTPUT_DIR"], exist_ok=True)

    from .routes import main
    app.register_blueprint(main)

    return app