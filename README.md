# MiProyecto (refactor - arquitectura modelo/manager/vista)

Estructura propuesta:
- modelos/: clases (Persona, Auto, Zapato, etc).
- managers/: lógica de negocio / acceso a BD. Métodos: insertar, buscar, listar, encontrar, borrar.
- vistas/
  - consola/: CLI que llama a los managers.
  - tui/: TUI interactiva en terminal (prompt_toolkit).
  - web/: app Flask que llama a los managers (no API).
- tests/: pruebas con pytest.

Instalación:
1. python -m venv venv
2. source venv/bin/activate  # o venv\Scripts\activate en Windows
3. pip install -r requirements.txt

Ejecutar consola:
- python -m vistas.consola.main --list
- python -m vistas.consola.main --add "Pedro" 40

Ejecutar TUI:
- pip install prompt_toolkit
- python -m vistas.tui.main

Ejecutar web:
- python -m vistas.web.app
  Abrir http://127.0.0.1:5000

Correr tests:
- pytest -q

Notas:
- Se usa SQLAlchemy como ORM para mapear clases a tablas.
- Template Method: modelos/report_template.py (PersonaReport).
- Los managers exponen insertar, buscar, listar, encontrar y borrar, tal como exige tu docente.
- CI sugerido: añadir un workflow que ejecute pytest y flake8 en cada PR.
