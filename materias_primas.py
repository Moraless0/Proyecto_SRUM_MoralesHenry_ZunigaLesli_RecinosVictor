from persistence import load_json, save_json
from validators import non_empty, positive_int, non_negative_float, unique_code, date
import inventario

FILE = "data/materias_primas.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def registrar():
    data = cargar()
    print("\n=== Registrar Materia Prima ===")

    while True:
        codigo = non_empty("Código: ")
        if unique_code(codigo, data, "codigo"):
            break
        print("⚠ Código repetido.")

    nombre = non_empty("Nombre: ")
    descripcion = non_empty("Descripción: ")
    proveedor = non_empty("Proveedor: ")
    stock = positive_int("Cantidad en stock: ")
    precio = non_negative_float("Precio por unidad: ")
    fecha_adquisicion = date("Fecha de adquisición (dd/mm/aaaa): ")
    fecha_vencimiento = date("Fecha de vencimiento (dd/mm/aaaa, Enter para omitir): ", optional=True)

    item = {
        "codigo": codigo,
        "nombre": nombre,
        "descripcion": descripcion,
        "proveedor": proveedor,
        "stock": stock,
        "precio": precio,
        "fecha_adquisicion": fecha_adquisicion,
        "fecha_vencimiento": fecha_vencimiento
    }

    data.append(item)
    guardar(data)
    inventario.sumar_materia(codigo, stock)
    print("✅ Registrado.")

def listar():
    data = cargar()
    print("\n=== Materias Primas ===")
    if not data:
        print("No hay registros.")
        return
    for m in data:
        print(f"\n  Código      : {m['codigo']}")
        print(f"  Nombre      : {m['nombre']}")
        print(f"  Descripción : {m['descripcion']}")
        print(f"  Proveedor   : {m['proveedor']}")
        print(f"  Stock       : {m['stock']}")
        print(f"  Precio/u    : Q{m['precio']}")
        print(f"  Adquisición : {m.get('fecha_adquisicion', '-')}")
        print(f"  Vencimiento : {m.get('fecha_vencimiento') or 'N/A'}")

def editar():
    data = cargar()
    codigo = non_empty("Código a editar: ")
    item = next((m for m in data if m["codigo"] == codigo), None)
    if not item:
        print("⚠ No encontrado.")
        return

    print(f"\nEditando '{item['nombre']}' — Enter para mantener valor actual:")
    v = input(f"  Nombre [{item['nombre']}]: ").strip()
    if v: item["nombre"] = v
    v = input(f"  Descripción [{item['descripcion']}]: ").strip()
    if v: item["descripcion"] = v
    v = input(f"  Proveedor [{item['proveedor']}]: ").strip()
    if v: item["proveedor"] = v
    v = input(f"  Stock [{item['stock']}]: ").strip()
    if v and v.isdigit() and int(v) > 0: item["stock"] = int(v)
    v = input(f"  Precio [{item['precio']}]: ").strip()
    if v:
        try:
            f = float(v)
            if f >= 0: item["precio"] = f
        except: pass
    v = input(f"  Fecha adquisición [{item.get('fecha_adquisicion','')}]: ").strip()
    if v: item["fecha_adquisicion"] = v
    v = input(f"  Fecha vencimiento [{item.get('fecha_vencimiento','')}]: ").strip()
    if v: item["fecha_vencimiento"] = v or None

    guardar(data)
    print("✅ Actualizado.")

def eliminar():
    data = cargar()
    codigo = non_empty("Código a eliminar: ")
    item = next((m for m in data if m["codigo"] == codigo), None)
    if not item:
        print("⚠ No encontrado.")
        return
    confirmar = input(f"¿Eliminar '{item['nombre']}'? (s/n): ").strip().lower()
    if confirmar == "s":
        data.remove(item)
        guardar(data)
        print("✅ Eliminado.")
    else:
        print("Cancelado.")