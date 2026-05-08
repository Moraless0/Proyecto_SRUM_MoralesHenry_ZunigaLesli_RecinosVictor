from persistence import load_json, save_json
from validators import non_empty, email, phone, unique_code

FILE = "data/clientes.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def _buscar_por_codigo(data, codigo):
    return next((c for c in data if c["codigo"] == codigo), None)

def registrar():
    data = cargar()
    print("\n=== Registrar Cliente ===")

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
    print("\n=== Clientes ===")
    if not data:
        print("No hay registros.")
        return
    for c in data:
     imprimir_resumen(c) # type: ignore

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
        print(f"⚠ Este cliente tiene {len(historial)} transacción(es) en historial.")
    confirmar = input(f"¿Eliminar '{item['empresa']}'? (s/n): ").strip().lower()
    if confirmar == "s":
        data.remove(item)
        guardar(data)
        print("✅ Eliminado.")
    else:
        print("Cancelado.")

def agregar_historial(codigo_cliente, entrada):
    data = cargar()
    cliente = _buscar_por_codigo(data, codigo_cliente)
    if cliente:
        cliente.setdefault("historial_transacciones", []).append(entrada)
        guardar(data)

def buscar():
    data = cargar()
    if not data:
        print("\nNo hay clientes registrados.")
        return

    print("\n=== Buscar Cliente ===")
    print("1. Por código")
    print("2. Por empresa")
    op = input("Opción: ").strip()

    if op == "1":
        codigo = non_empty("Código: ")
        item = _buscar_por_codigo(data, codigo)
        if not item:
            print("⚠ No encontrado.")
            return
        imprimir_detalle(item) 
    elif op == "2":
        empresa = non_empty("Empresa (parte o completo): ").lower()
        encontrados = [c for c in data if empresa in c["empresa"].lower()]
        if not encontrados:
            print("⚠ No se encontraron coincidencias.")
            return
        for c in encontrados:
         imprimir_detalle(c) 
    else:
        print("⚠ Opción inválida.")