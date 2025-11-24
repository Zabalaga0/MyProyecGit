import sys
from datetime import datetime
from managers.producto_manager import ProductoManager

def menu():
    print("╔════════════════════════════════════════════╗")
    print("║        🏪 SISTEMA DE GESTIÓN DE PRODUCTOS  ║")
    print("╠════════════════════════════════════════════╣")
    print("║ 1. 📝 Listar productos                     ║")
    print("║ 2. 🛒 Agregar producto                     ║")
    print("║ 3. ✏️  Modificar producto                   ║")
    print("║ 4. 💣 Eliminar producto                    ║")
    print("║ 5. 📆 Ver productos próximos a vencer      ║")
    print("║ 6. 🗿 Salir                                ║")
    print("╚════════════════════════════════════════════╝")

def input_date(prompt_text):
    s = input(prompt_text + " (YYYY-MM-DD) o Enter para vacio: ").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except:
        print("Formato inválido. Usa YYYY-MM-DD.")
        return input_date(prompt_text)

def listar(manager):
    productos = manager.listar()
    if not productos:
        print("(sin productos)")
        return
    for p in productos:
        print(f"{p.id}: {p.nombre} | Precio: {p.precio} | Cant: {p.cantidad} | Vence: {p.fecha_vencimiento}")

def agregar(manager):
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripcion: ").strip() or None
    precio = float(input("Precio: ").strip() or 0)
    cantidad = int(input("Cantidad: ").strip() or 0)
    fv = input_date("Fecha de vencimiento")
    p = manager.insertar(nombre=nombre, precio=precio, cantidad=cantidad, descripcion=descripcion, fecha_vencimiento=fv)
    print("Producto agregado:", p)

def modificar(manager):
    try:
        pid = int(input("ID del producto a modificar: ").strip())
    except:
        print("ID inválido.")
        return
    p = manager.buscar(pid)
    if not p:
        print("Producto no encontrado.")
        return
    print("Dejar en blanco para mantener valor actual.")
    nombre = input(f"Nombre [{p.nombre}]: ").strip() or p.nombre
    descripcion = input(f"Descripcion [{p.descripcion}]: ").strip() or p.descripcion
    precio_s = input(f"Precio [{p.precio}]: ").strip()
    precio = float(precio_s) if precio_s else p.precio
    cantidad_s = input(f"Cantidad [{p.cantidad}]: ").strip()
    cantidad = int(cantidad_s) if cantidad_s else p.cantidad
    fv = input_date("Fecha de vencimiento")
    if fv is None:
        fv = p.fecha_vencimiento
    manager.modificar(pid, nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, fecha_vencimiento=fv)
    print("Producto actualizado.")

def eliminar(manager):
    try:
        pid = int(input("ID del producto a eliminar: ").strip())
    except:
        print("ID inválido.")
        return
    ok = manager.eliminar(pid)
    print("Eliminado." if ok else "No existe.")

def ver_vencer(manager):
    dias_s = input("Ver próximos a vencer en cuántos días? (por defecto 30): ").strip()
    dias = int(dias_s) if dias_s else 30
    lista = manager.proximos_a_vencer(dias=dias)
    if not lista:
        print("(no hay productos próximos a vencer en ese rango)")
    for p in lista:
        print(f"{p.id}: {p.nombre} | Vence: {p.fecha_vencimiento} | Cant: {p.cantidad}")

def main():
    manager = ProductoManager()
    try:
        while True:
            menu()
            opcion = input("Opción: ").strip()
            if opcion == "1":
                listar(manager)
            elif opcion == "2":
                agregar(manager)
            elif opcion == "3":
                modificar(manager)
            elif opcion == "4":
                eliminar(manager)
            elif opcion == "5":
                ver_vencer(manager)
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
    finally:
        manager.cerrar()

if __name__ == "__main__":
    main()