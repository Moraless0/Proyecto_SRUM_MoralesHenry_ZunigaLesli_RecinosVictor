from persistence import load_json, save_json
from validators import non_empty, email, phone, unique_code

FILE = "data/clientes.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def _buscar_por_codigo(data, codigo):
    return next((c for c in data if c["codigo"] == codigo), None)
