from persistence import load_json, save_json
from validators import non_empty, email, phone, unique_code

FILE = "data/proveedores.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)
    

def _buscar_por_codigo(data, codigo):
    return next((p for p in data if p["codigo"] == codigo), None)

def registrar():
    data = cargar()
    print("\n=== Registrar Proveedor ===")

    while True:
        codigo = non_empty("Código: ")
        if unique_code(codigo, data, "codigo"):
            break
        print("⚠ Código repetido.")

    empresa = non_empty("Empresa: ")
    contacto = non_empty("Contacto: ")
    direccion = non_empty("Dirección: ")
    tel_cel = phone("Teléfono celular: ")
    tel_fijo = phone("Teléfono fijo: ")
    correo = email("Correo: ")

    item = {
        "codigo": codigo,
        "empresa": empresa,
        "contacto": contacto,
        "direccion": direccion,
        "tel_cel": tel_cel,
        "tel_fijo": tel_fijo,
        "correo": correo,
        "historial_transacciones": []
    }

    data.append(item)
    guardar(data)
    print("✅ Registrado.")

def listar():
    data = cargar()
    print("\n=== Proveedores ===")
    if not data:
        print("No hay registros.")
        return
    for p in data:
        _imprimir_resumen(p)