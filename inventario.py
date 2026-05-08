from persistence import load_json, save_json

FILE = "data/inventario.json"   # ← RUTA ACTUALIZADA

def cargar():
    return load_json(FILE, {"materias": {}, "productos": {}})

def guardar(data):
    save_json(FILE, data)

def sumar_materia(codigo, cantidad):
    inv = cargar()
    inv["materias"][codigo] = inv["materias"].get(codigo, 0) + cantidad
    guardar(inv)

def restar_materia(codigo, cantidad):
    inv = cargar()
    actual = inv["materias"].get(codigo, 0)
    nuevo = max(0, actual - cantidad)
    inv["materias"][codigo] = nuevo
    guardar(inv)

def sumar_producto(codigo, cantidad):
    inv = cargar()
    inv["productos"][codigo] = inv["productos"].get(codigo, 0) + cantidad
    guardar(inv)

def restar_producto(codigo, cantidad):
    inv = cargar()
    actual = inv["productos"].get(codigo, 0)
    nuevo = max(0, actual - cantidad)
    inv["productos"][codigo] = nuevo
    guardar(inv)

def tiene_stock_materia(codigo, cantidad):
    inv = cargar()
    return inv["materias"].get(codigo, 0) >= cantidad

def tiene_stock_producto(codigo, cantidad):
    inv = cargar()
    return inv["productos"].get(codigo, 0) >= cantidad

def mostrar():
    inv = cargar()
    print("\n=== Inventario ===")
    print("Materias primas:")
    if not inv["materias"]:
        print("  (Sin registros)")
    else:
        for k, v in inv["materias"].items():
            print(f"  {k}: {v}")
    print("\nProductos finales:")
    if not inv["productos"]:
        print("  (Sin registros)")
    else:
        for k, v in inv["productos"].items():
            print(f"  {k}: {v}")