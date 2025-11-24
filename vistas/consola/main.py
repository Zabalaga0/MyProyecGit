import argparse
from managers.persona_manager import PersonaManager
from modelos.report_template import PersonaReport

def main():
    parser = argparse.ArgumentParser(prog="mi_proyecto")
    parser.add_argument("--add", nargs=2, metavar=("NOMBRE","EDAD"), help="Agregar persona")
    parser.add_argument("--list", action="store_true", help="Listar personas")
    args = parser.parse_args()

    manager = PersonaManager()  # usa sqlite local personas.db
    try:
        if args.add:
            nombre, edad = args.add
            p = manager.insertar(nombre, int(edad))
            print("Insertada:", p)
        elif args.list:
            report = PersonaReport(manager)
            print(report.generar_reporte())
        else:
            parser.print_help()
    finally:
        manager.cerrar()

if __name__ == "__main__":
    main()
