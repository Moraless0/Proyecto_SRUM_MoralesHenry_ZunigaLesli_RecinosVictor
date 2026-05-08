import materias_primas
import proveedores
import productos
import clientes
import produccion
import ventas
import inventario
import reportes

def menu():
    while True:
        print("\n=== Sistema de Manufactura IAQ ===")
        print("1. Materias primas")
        print("2. Proveedores")
        print("3. Productos finales")
        print("4. Clientes")
        print("5. Producción")
        print("6. Ventas")
        print("7. Inventario")
        print("8. Reportes")
        print("0. Salir")

        op = input("Opción: ").strip()

        if op == "1":
            materias_menu()
        elif op == "2":
            proveedores_menu()
        elif op == "3":
            productos_menu()
        elif op == "4":
            clientes_menu()
        elif op == "5":
            produccion_menu()
        elif op == "6":
            ventas_menu()
        elif op == "7":
            inventario.mostrar()
        elif op == "8":
            reportes.menu()
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("⚠ Opción inválida.")

def materias_menu():
    while True:
        print("\n=== Materias Primas ===")
        print("1. Registrar")
        print("2. Listar")
        print("3. Editar")
        print("4. Eliminar")
        print("5. Buscar")
        print("6. Ver detalle")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            materias_primas.registrar()
        elif op == "2":
            materias_primas.listar()
        elif op == "3":
            materias_primas.editar()
        elif op == "4":
            materias_primas.eliminar()
        elif op == "5":
            if hasattr(materias_primas, "buscar"):
                materias_primas.buscar()
            else:
                print("Función de búsqueda no implementada.")
        elif op == "6":
            if hasattr(materias_primas, "ver_detalle"):
                materias_primas.ver_detalle()
            else:
                print("Función de detalle no implementada.")
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

def proveedores_menu():
    while True:
        print("\n=== Proveedores ===")
        print("1. Registrar")
        print("2. Listar")
        print("3. Editar")
        print("4. Eliminar")
        print("5. Buscar")
        print("6. Ver detalle")
        print("7. Ver historial")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            proveedores.registrar()
        elif op == "2":
            proveedores.listar()
        elif op == "3":
            proveedores.editar()
        elif op == "4":
            proveedores.eliminar()
        elif op == "5":
            proveedores.buscar()
        elif op == "6":
            proveedores.ver_detalle()
        elif op == "7":
            proveedores.ver_historial()
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

def productos_menu():
    while True:
        print("\n=== Productos Finales ===")
        print("1. Registrar")
        print("2. Listar")
        print("3. Editar")
        print("4. Eliminar")
        print("5. Buscar")
        print("6. Ver detalle")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            productos.registrar()
        elif op == "2":
            productos.listar()
        elif op == "3":
            productos.editar()
        elif op == "4":
            productos.eliminar()
        elif op == "5":
            productos.buscar()
        elif op == "6":
            productos.ver_detalle()
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

def clientes_menu():
    while True:
        print("\n=== Clientes ===")
        print("1. Registrar")
        print("2. Listar")
        print("3. Editar")
        print("4. Eliminar")
        print("5. Buscar")
        print("6. Ver detalle")
        print("7. Ver historial")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            clientes.registrar()
        elif op == "2":
            clientes.listar()
        elif op == "3":
            clientes.editar()
        elif op == "4":
            clientes.eliminar()
        elif op == "5":
            clientes.buscar()
        elif op == "6":
            clientes.ver_detalle()
        elif op == "7":
            clientes.ver_historial()
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

def produccion_menu():
    while True:
        print("\n=== Producción ===")
        print("1. Registrar orden")
        print("2. Listar órdenes")
        print("3. Cambiar estado")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            produccion.registrar()
        elif op == "2":
            produccion.listar()
        elif op == "3":
            produccion.cambiar_estado()
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

def ventas_menu():
    while True:
        print("\n=== Ventas ===")
        print("1. Registrar orden")
        print("2. Listar órdenes")
        print("3. Cambiar estado")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            ventas.registrar()
        elif op == "2":
            ventas.listar()
        elif op == "3":
            ventas.cambiar_estado()
        elif op == "0":
            break
        else:
            print("⚠ Opción inválida.")

if __name__ == "__main__":
    menu()
