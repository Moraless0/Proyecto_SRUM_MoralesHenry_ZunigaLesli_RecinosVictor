from persistence import load_json, save_json
from validators import non_empty, non_negative_float, positive_int, unique_code, date
import inventario

FILE = "data/productos.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def _buscar_por_codigo(data, codigo):
    return next((p for p in data if p["codigo"] == codigo), None)

def registrar():
    data = cargar()
    print("\n=== Registrar Producto Final ===")

    while True:
        codigo = non_empty("Código: ")
        if unique_code(codigo, data, "codigo"):
            break
        print("⚠ Código repetido.")

    nombre = non_empty("Nombre: ")
    descripcion = non_empty("Descripción: ")
    precio = non_negative_float("Precio de venta: ")
    stock = positive_int("Stock inicial: ")
    fecha_fabricacion = date("Fecha de fabricación (dd/mm/aaaa): ")
    fecha_vencimiento = date("Fecha de vencimiento (dd/mm/aaaa, Enter para omitir): ", optional=True)

    item = {
        "codigo": codigo,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "fecha_fabricacion": fecha_fabricacion,
        "fecha_vencimiento": fecha_vencimiento
    }

    data.append(item)
    guardar(data)
    inventario.sumar_producto(codigo, stock)
    print("✅ Registrado.")

def listar():
    data = cargar()
    print("\n=== Productos Finales ===")
    if not data:
        print("No hay registros.")
        return
    for p in data:
        print(f"\n  Código       : {p['codigo']}")
        print(f"  Nombre       : {p['nombre']}")
        print(f"  Descripción  : {p['descripcion']}")
        print(f"  Precio venta : Q{p['precio']}")
        print(f"  Stock        : {p['stock']}")
        print(f"  Fabricación  : {p.get('fecha_fabricacion', '-')}")
        print(f"  Vencimiento  : {p.get('fecha_vencimiento') or 'N/A'}")

def editar():
    data = cargar()
    codigo = non_empty("Código a editar: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return

    stock_anterior = item.get("stock", 0)

    print(f"\nEditando '{item['nombre']}' — Enter para mantener valor actual:")
    v = input(f"  Nombre [{item['nombre']}]: ").strip()
    if v:
        item["nombre"] = v
    v = input(f"  Descripción [{item['descripcion']}]: ").strip()
    if v:
        item["descripcion"] = v
    v = input(f"  Precio [{item['precio']}]: ").strip()
    if v:
        try:
            f = float(v)
            if f >= 0:
                item["precio"] = f
            else:
                print("⚠ Precio inválido, se mantiene el anterior.")
        except ValueError:
            print("⚠ Valor no numérico, se mantiene el anterior.")
    v = input(f"  Stock [{item['stock']}]: ").strip()
    if v:
        try:
            nuevo_stock = int(v)
            if nuevo_stock >= 0:
                item["stock"] = nuevo_stock
            else:
                print("⚠ Stock inválido, se mantiene el anterior.")
        except ValueError:
            print("⚠ Valor no numérico, se mantiene el anterior.")
    v = input(f"  Fecha fabricación [{item.get('fecha_fabricacion','')}]: ").strip()
    if v:
        item["fecha_fabricacion"] = v
    v = input(f"  Fecha vencimiento [{item.get('fecha_vencimiento','')}]: ").strip()
    if v:
        item["fecha_vencimiento"] = v or None

    guardar(data)

    # Sincronizar inventario si cambió el stock
    nuevo_stock = item.get("stock", stock_anterior)
    diferencia = nuevo_stock - stock_anterior
    if diferencia != 0:
        inventario.sumar_producto(codigo, diferencia)

    print("✅ Actualizado.")

def eliminar():
    data = cargar()
    codigo = non_empty("Código a eliminar: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return
    confirmar = input(f"¿Eliminar '{item['nombre']}'? (s/n): ").strip().lower()
    if confirmar == "s":
        # Descontar del inventario el stock existente
        stock_actual = item.get("stock", 0)
        if stock_actual > 0:
            inventario.restar_producto(codigo, stock_actual)
        data.remove(item)
        guardar(data)
        print("✅ Eliminado.")
    else:
        print("Cancelado.")

def buscar():
    data = cargar()
    if not data:
        print("\nNo hay productos registrados.")
        return

    print("\n=== Buscar Producto ===")
    print("1. Por código")
    print("2. Por nombre")
    op = input("Opción: ").strip()

    if op == "1":
        codigo = non_empty("Código: ")
        item = _buscar_por_codigo(data, codigo)
        if not item:
            print("⚠ No encontrado.")
            return
        _imprimir_detalle(item)
    elif op == "2":
        nombre = non_empty("Nombre (parte o completo): ").lower()
        encontrados = [p for p in data if nombre in p["nombre"].lower()]
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
        print("\nNo hay productos registrados.")
        return
    codigo = non_empty("Código del producto: ")
    item = _buscar_por_codigo(data, codigo)
    if not item:
        print("⚠ No encontrado.")
        return
    print("\n=== Detalle del Producto ===")
    _imprimir_detalle(item)

def _imprimir_detalle(p):
    print(f"\n  Código       : {p['codigo']}")
    print(f"  Nombre       : {p['nombre']}")
    print(f"  Descripción  : {p['descripcion']}")
    print(f"  Precio venta : Q{p['precio']}")
    print(f"  Stock        : {p['stock']}")
    print(f"  Fabricación  : {p.get('fecha_fabricacion', '-')}")
    print(f"  Vencimiento  : {p.get('fecha_vencimiento') or 'N/A'}")