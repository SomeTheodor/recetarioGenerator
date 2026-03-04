import json

def load_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(json_path, data):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_receta_by_id(data, receta_id):
    return next((r for r in data["recetas"] if r["id"] == receta_id), None)