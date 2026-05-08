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

def ver_historial():
    data = cargar()
    if not data:
        print("\nNo hay proveedores registrados.")
        return
    codigo = non_empty("Código del proveedor: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return
    historial = item.get("historial_transacciones", [])
    print(f"\n=== Historial de '{item['empresa']}' ===")
    if not historial:
        print("Sin transacciones registradas.")
        return
    for h in historial:
        print(f"  > {h}")

def _imprimir_resumen(p):
    historial = p.get("historial_transacciones", [])
    print(f"\n  Código    : {p['codigo']}")
    print(f"  Empresa   : {p['empresa']}")
    print(f"  Contacto  : {p['contacto']}")
    print(f"  Dirección : {p['direccion']}")
    print(f"  Celular   : {p['tel_cel']}")
    print(f"  Fijo      : {p['tel_fijo']}")
    print(f"  Correo    : {p['correo']}")
    print(f"  Historial : {len(historial)} transacción(es)")

def _imprimir_detalle(p):
    _imprimir_resumen(p)
    historial = p.get("historial_transacciones", [])
    if historial:
        print("\n  Detalle de historial:")
        for h in historial:
            print(f"    > {h}")