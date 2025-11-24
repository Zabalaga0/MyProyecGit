"""
TUI simple con prompt_toolkit que llama a PersonaManager.
Ejecutar: python -m vistas.tui.main
Dependencia: prompt_toolkit
"""
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from managers.persona_manager import PersonaManager

MENU = ["listar", "agregar", "buscar", "borrar", "salir"]
completer = WordCompleter(MENU, ignore_case=True)

def run():
    manager = PersonaManager()
    try:
        while True:
            cmd = prompt("Comando (listar/agregar/buscar/borrar/salir)> ", completer=completer).strip().lower()
            if cmd == "listar":
                personas = manager.listar()
                if not personas:
                    print("(sin personas)")
                for p in personas:
                    print(f"{{p.id}}: {{p.nombre}} ({{p.edad}})")
            elif cmd == "agregar":
                nombre = prompt("Nombre: ").strip()
                edad = prompt("Edad: ").strip()
                try:
                    p = manager.insertar(nombre, int(edad))
                    print("Insertada:", p)
                except Exception as e:
                    print("Error al insertar:", e)
            elif cmd == "buscar":
                id_s = prompt("ID a buscar: ").strip()
                try:
                    p = manager.buscar(int(id_s))
                    print(p if p else "No encontrada")
                except:
                    print("ID inválido")
            elif cmd == "borrar":
                id_s = prompt("ID a borrar: ").strip()
                try:
                    ok = manager.borrar(int(id_s))
                    print("Borrada" if ok else "No existe")
                except:
                    print("ID inválido")
            elif cmd == "salir":
                break
            else:
                print("Comando no reconocido.")
    finally:
        manager.cerrar()

if __name__ == "__main__":
    run()
