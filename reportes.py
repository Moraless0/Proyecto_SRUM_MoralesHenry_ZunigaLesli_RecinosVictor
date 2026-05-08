import materias_primas
import proveedores
import productos
import clientes
import produccion
import ventas
import inventario

def menu():
    while True:
        print("\n=== Reportes ===")
        print("1. Materias primas en stock")
        print("2. Proveedores e historial")
        print("3. Órdenes de producción")
        print("4. Productos finales en stock")
        print("5. Clientes e historial")
        print("6. Órdenes de venta")
        print("7. Inventario general")
        print("0. Volver")

        op = input("Opción: ").strip()

        if op == "1":
            materias_primas.listar()
        elif op == "2":
            reporte_proveedores()
        elif op == "3":
            reporte_ordenes_produccion()
        elif op == "4":
            productos.listar()
        elif op == "5":
            reporte_clientes()
        elif op == "6":
            reporte_ordenes_venta()
        elif op == "7":
            inventario.mostrar()
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

def reporte_proveedores():
    data = proveedores.cargar()
    print("\n=== Proveedores ===")
    if not data:
        print("No hay registros.")
        return
    for p in data:
        print(f"{p['codigo']} - {p['empresa']} | {p['correo']}")
        historial = p.get("historial_transacciones", [])
        if historial:
            for t in historial:
                print(f"  > {t}")
        else:
            print("  (Sin historial)")

def reporte_clientes():
    data = clientes.cargar()
    print("\n=== Clientes ===")
    if not data:
        print("No hay registros.")
        return
    for c in data:
        print(f"{c['codigo']} - {c['empresa']} | {c['correo']}")
        historial = c.get("historial_transacciones", [])
        if historial:
            for t in historial:
                print(f"  > {t}")
        else:
            print("  (Sin historial)")

def reporte_ordenes_produccion():
    print("\n=== Reporte de Órdenes de Producción ===")
    # Se delega al módulo produccion; se asume que listar muestra estado, fechas, etc.
    try:
        produccion.listar()
    except Exception as e:
        print(f"Error al generar reporte de producción: {e}")

def reporte_ordenes_venta():
    print("\n=== Reporte de Órdenes de Venta ===")
    # Se delega al módulo ventas; se asume que listar muestra estado, fechas, etc.
    try:
        ventas.listar()
    except Exception as e:
        print(f"Error al generar reporte de ventas: {e}")