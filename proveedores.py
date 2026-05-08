from persistence import load_json, save_json
from validators import non_empty, email, phone, unique_code

FILE = "data/proveedores.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def _buscar_por_codigo(data, codigo):
    return next((p for p in data if p["codigo"] == codigo), None)