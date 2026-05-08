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

def editar():
    data = cargar()
    codigo = non_empty("Código a editar: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return

    print(f"\nEditando '{item['empresa']}' — Enter para mantener valor actual:")
    v = input(f"  Empresa [{item['empresa']}]: ").strip()
    if v:
        item["empresa"] = v
    v = input(f"  Contacto [{item['contacto']}]: ").strip()
    if v:
        item["contacto"] = v
    v = input(f"  Dirección [{item['direccion']}]: ").strip()
    if v:
        item["direccion"] = v
    v = input(f"  Celular [{item['tel_cel']}]: ").strip()
    if v:
        item["tel_cel"] = v
    v = input(f"  Fijo [{item['tel_fijo']}]: ").strip()
    if v:
        item["tel_fijo"] = v
    v = input(f"  Correo [{item['correo']}]: ").strip()
    if v:
        item["correo"] = v

    guardar(data)
    print("✅ Actualizado.")