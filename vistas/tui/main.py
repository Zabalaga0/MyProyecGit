"""
TUI simple con prompt_toolkit que llama a ProductoManager.
Ejecutar: python -m vistas.tui.main
Dependencia: prompt_toolkit
"""
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from managers.producto_manager import ProductoManager
from datetime import datetime

MENU = ["listar", "agregar", "modificar", "eliminar", "vencer", "salir"]
completer = WordCompleter(MENU, ignore_case=True)

def input_date(prompt_text):
    s = prompt(prompt_text + " (YYYY-MM-DD) o Enter para vacio: ").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except:
        print("Formato inválido.")
        return input_date(prompt_text)

def run():
    manager = ProductoManager()
    try:
        while True:
            cmd = prompt("Comando (listar/agregar/modificar/eliminar/vencer/salir)> ", completer=completer).strip().lower()
            if cmd == "listar":
                for p in manager.listar():
                    print(f"{p.id}: {p.nombre} | Precio:{p.precio} | Cant:{p.cantidad} | Vence:{p.fecha_vencimiento}")
            elif cmd == "agregar":
                nombre = prompt("Nombre: ").strip()
                descripcion = prompt("Descripcion: ").strip() or None
                precio = float(prompt("Precio: ").strip() or 0)
                cantidad = int(prompt("Cantidad: ").strip() or 0)
                fv = input_date("Fecha de vencimiento")
                p = manager.insertar(nombre=nombre, precio=precio, cantidad=cantidad, descripcion=descripcion, fecha_vencimiento=fv)
                print("Insertada:", p)
            elif cmd == "modificar":
                try:
                    pid = int(prompt("ID: ").strip())
                except:
                    print("ID inválido")
                    continue
                p = manager.buscar(pid)
                if not p:
                    print("No existe")
                    continue
                nombre = prompt(f"Nombre [{p.nombre}]: ").strip() or p.nombre
                descripcion = prompt(f"Descripcion [{p.descripcion}]: ").strip() or p.descripcion
                precio_s = prompt(f"Precio [{p.precio}]: ").strip()
                precio = float(precio_s) if precio_s else p.precio
                cantidad_s = prompt(f"Cantidad [{p.cantidad}]: ").strip()
                cantidad = int(cantidad_s) if cantidad_s else p.cantidad
                fv = input_date("Fecha de vencimiento")
                if fv is None:
                    fv = p.fecha_vencimiento
                manager.modificar(pid, nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, fecha_vencimiento=fv)
                print("Actualizado.")
            elif cmd == "eliminar":
                try:
                    pid = int(prompt("ID: ").strip())
                except:
                    print("ID inválido")
                    continue
                ok = manager.eliminar(pid)
                print("Eliminado." if ok else "No existe.")
            elif cmd == "vencer":
                dias = int(prompt("Dias (default 30): ").strip() or 30)
                for p in manager.proximos_a_vencer(dias=dias):
                    print(f"{p.id}: {p.nombre} | Vence: {p.fecha_vencimiento} | Cant: {p.cantidad}")
            elif cmd == "salir":
                break
            else:
                print("Comando no reconocido.")
    finally:
        manager.cerrar()

if __name__ == "__main__":
    run()