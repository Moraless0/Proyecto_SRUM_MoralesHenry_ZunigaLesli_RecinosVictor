from persistence import load_json, save_json
from validators import non_empty, email, phone, unique_code

FILE = "data/proveedores.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def _buscar_por_codigo(data, codigo):
    return next((p for p in data if p["codigo"] == codigo), None)

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

def eliminar():
    data = cargar()
    codigo = non_empty("Código a eliminar: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return

    historial = item.get("historial_transacciones", [])
    if historial:
        print(f"⚠ Este proveedor tiene {len(historial)} transacción(es) en historial.")
    confirmar = input(f"¿Eliminar '{item['empresa']}'? (s/n): ").strip().lower()
    if confirmar == "s":
        data.remove(item)
        guardar(data)
        print("✅ Eliminado.")
    else:
        print("Cancelado.")

def agregar_historial(codigo_proveedor, entrada):
    data = cargar()
    proveedor = _buscar_por_codigo(data, codigo_proveedor)
    if proveedor:
        proveedor.setdefault("historial_transacciones", []).append(entrada)
        guardar(data)

def buscar():
    data = cargar()
    if not data:
        print("\nNo hay proveedores registrados.")
        return

    print("\n=== Buscar Proveedor ===")
    print("1. Por código")
    print("2. Por empresa")
    op = input("Opción: ").strip()

    if op == "1":
        codigo = non_empty("Código: ")
        item = _buscar_por_codigo(data, codigo)
        if not item:
            print("⚠ No encontrado.")
            return
        _imprimir_detalle(item)
    elif op == "2":
        empresa = non_empty("Empresa (parte o completo): ").lower()
        encontrados = [p for p in data if empresa in p["empresa"].lower()]
        if not encontrados:
            print("⚠ No se encontraron coincidencias.")
            return
        for p in encontrados:
            _imprimir_detalle(p)
    else:
        print("⚠ Opción inválida.")

def ver_detalle():
    data = cargar()
    if not data:
        print("\nNo hay proveedores registrados.")
        return
    codigo = non_empty("Código del proveedor: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return
    print("\n=== Detalle del Proveedor ===")
    _imprimir_detalle(item)