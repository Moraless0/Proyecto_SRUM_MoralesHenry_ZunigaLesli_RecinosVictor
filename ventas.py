from persistence import load_json, save_json
from validators import non_empty, positive_int, unique_code, date
import clientes
import productos
import inventario

FILE = "data/ventas.json"   # ← RUTA ACTUALIZADA

ESTADOS_VALIDOS = ["Pendiente", "En Proceso", "Enviado", "Entregado", "Cancelado"]

def cargar():
    return load_json(FILE, [])

def guardar(data):
    save_json(FILE, data)

def registrar():
    data = cargar()
    cli = clientes.cargar()
    prods = productos.cargar()

    print("\n=== Registrar Orden de Venta ===")

    while True:
        codigo = non_empty("Código: ")
        if unique_code(codigo, data, "codigo"):
            break
        print("⚠ Código repetido.")

    print("\nClientes disponibles:")
    for c in cli:
        print(f"  {c['codigo']} - {c['empresa']}")

    cod_cli = non_empty("Código cliente: ")
    cliente = next((c for c in cli if c["codigo"] == cod_cli), None)
    if not cliente:
        print("⚠ Cliente no encontrado.")
        return

    print("\nProductos disponibles:")
    for p in prods:
        print(f"  {p['codigo']} - {p['nombre']} (Stock: {p['stock']})")

    items = []
    total = 0

    print("\nIngrese productos (vacío para terminar):")
    while True:
        cod_prod = input("  Código producto: ").strip()
        if cod_prod == "":
            break
        prod = next((p for p in prods if p["codigo"] == cod_prod), None)
        if not prod:
            print("  ⚠ No existe.")
            continue
        cant = positive_int("  Cantidad: ")
        subtotal = cant * prod["precio"]
        total += subtotal
        items.append({"codigo": cod_prod, "cantidad": cant, "subtotal": subtotal})

    fecha_creacion = date("Fecha de creación (dd/mm/aaaa): ")
    fecha_entrega_estimada = date("Fecha de entrega estimada (dd/mm/aaaa): ")

    orden = {
        "codigo": codigo,
        "cliente": cod_cli,
        "items": items,
        "total": total,
        "fecha_creacion": fecha_creacion,
        "fecha_entrega_estimada": fecha_entrega_estimada,
        "estado": "Pendiente"
    }

    data.append(orden)
    guardar(data)
    clientes.agregar_historial(cod_cli, f"Orden {codigo} — Q{total} — {fecha_creacion}")
    print(f"✅ Orden registrada. Total: Q{total}")

def listar():
    data = cargar()
    print("\n=== Órdenes de Venta ===")
    if not data:
        print("No hay registros.")
        return
    for o in data:
        print(f"\n  Código          : {o['codigo']}")
        print(f"  Cliente         : {o['cliente']}")
        print(f"  Total           : Q{o['total']}")
        print(f"  Fecha creación  : {o.get('fecha_creacion', '-')}")
        print(f"  Entrega est.    : {o.get('fecha_entrega_estimada', '-')}")
        print(f"  Estado          : {o['estado']}")
        for it in o.get("items", []):
            print(f"    - {it['codigo']} × {it['cantidad']} = Q{it['subtotal']}")

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

    if orden["estado"] not in ["Enviado", "Entregado"] and nuevo in ["Enviado", "Entregado"]:
        inv = inventario.cargar()
        prods = productos.cargar()
        for item in orden["items"]:
            disponible = inv["productos"].get(item["codigo"], 0)
            if disponible < item["cantidad"]:
                prod = next((p for p in prods if p["codigo"] == item["codigo"]), None)
                nombre = prod["nombre"] if prod else item["codigo"]
                print(f"⚠ Stock insuficiente de '{nombre}': disponible {disponible}, requerido {item['cantidad']}.")
                return
        for item in orden["items"]:
            inventario.sumar_producto(item["codigo"], -item["cantidad"])

    orden["estado"] = nuevo
    guardar(data)
    print("✅ Estado actualizado.")