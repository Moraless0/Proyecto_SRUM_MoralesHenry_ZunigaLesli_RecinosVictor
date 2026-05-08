
from persistence import load_json, save_json
from validators import non_empty, positive_int, unique_code, date
import inventario
import materias_primas
import productos

FILE = "data/produccion.json"   # ← RUTA ACTUALIZADA

ESTADOS_VALIDOS = ["Pendiente", "En Proceso", "Completada", "Cancelada"]

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def registrar():
    data = cargar()
    mats = materias_primas.cargar()
    prods = productos.cargar()

    print("\n=== Registrar Orden de Producción ===")

    while True:
        codigo = non_empty("Código: ")
        if unique_code(codigo, data, "codigo"):
            break
        print("⚠ Código repetido.")

    print("\nProductos disponibles:")
    for p in prods:
        print(f"  {p['codigo']} - {p['nombre']}")

    cod_prod = non_empty("Código del producto a fabricar: ")
    prod = next((p for p in prods if p["codigo"] == cod_prod), None)
    if not prod:
        print("⚠ Producto no encontrado.")
        return

    cantidad = positive_int("Cantidad a producir: ")

    print("\nMaterias primas disponibles:")
    for m in mats:
        print(f"  {m['codigo']} - {m['nombre']} (Stock: {m['stock']})")

    requeridas = []
    print("\nIngrese materias primas requeridas (vacío para terminar):")
    while True:
        cod_mat = input("  Código materia prima: ").strip()
        if cod_mat == "":
            break
        mat = next((m for m in mats if m["codigo"] == cod_mat), None)
        if not mat:
            print("  ⚠ No existe.")
            continue
        cant = positive_int("  Cantidad requerida: ")
        requeridas.append({"codigo": cod_mat, "cantidad": cant})

    fecha_inicio = date("Fecha de inicio (dd/mm/aaaa): ")
    fecha_fin_estimada = date("Fecha de finalización estimada (dd/mm/aaaa): ")

    orden = {
        "codigo": codigo,
        "producto": cod_prod,
        "cantidad": cantidad,
        "materias": requeridas,
        "fecha_inicio": fecha_inicio,
        "fecha_fin_estimada": fecha_fin_estimada,
        "estado": "Pendiente"
    }

    data.append(orden)
    guardar(data)
    print("✅ Orden registrada.")

def listar():
    data = cargar()
    print("\n=== Órdenes de Producción ===")
    if not data:
        print("No hay registros.")
        return
    for o in data:
        print(f"\n  Código     : {o['codigo']}")
        print(f"  Producto   : {o['producto']}")
        print(f"  Cantidad   : {o['cantidad']}")
        print(f"  Inicio     : {o.get('fecha_inicio', '-')}")
        print(f"  Fin est.   : {o.get('fecha_fin_estimada', '-')}")
        print(f"  Estado     : {o['estado']}")
        mats = o.get("materias", [])
        if mats:
            print(f"  Materias   : " + ", ".join(f"{m['codigo']}×{m['cantidad']}" for m in mats))

def cambiar_estado():
    data = cargar()
    codigo = non_empty("Código de orden: ")
    orden = next((o for o in data if o["codigo"] == codigo), None)

    if not orden:
        print("⚠ No existe.")
        return

    print(f"  Estado actual: {orden['estado']}")
    print(f"  Estados válidos: {', '.join(ESTADOS_VALIDOS)}")
    nuevo = non_empty("Nuevo estado: ")

    if nuevo not in ESTADOS_VALIDOS:
        print("⚠ Estado inválido.")
        return

    if orden["estado"] != "Completada" and nuevo == "Completada":
        inv = inventario.cargar()
        for m in orden["materias"]:
            disponible = inv["materias"].get(m["codigo"], 0)
            if disponible < m["cantidad"]:
                mat = next((mp for mp in materias_primas.cargar() if mp["codigo"] == m["codigo"]), None)
                nombre = mat["nombre"] if mat else m["codigo"]
                print(f"⚠ Stock insuficiente de '{nombre}': disponible {disponible}, requerido {m['cantidad']}.")
                return
        for m in orden["materias"]:
            inventario.sumar_materia(m["codigo"], -m["cantidad"])
        inventario.sumar_producto(orden["producto"], orden["cantidad"])

    orden["estado"] = nuevo
    guardar(data)
    print("✅ Estado actualizado.")