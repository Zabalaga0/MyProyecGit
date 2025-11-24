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
1. 
```powershell
python -m venv venv
```
2. source venv/bin/activate  # o 
```powershell
venv\Scripts\activate
```
en Windows
3. 
```powershell
pip install -r requirements.txt
```
### EJECUCIONES
Ejecutar consola:
```powershell
python -m vistas.consola.main
```

Ejecutar TUI:
```powershell
pip install prompt_toolkit
```
ejecutar
```powershell
python -m vistas.tui.main
```

Correr tests:
```powershell
pytest -q
```

Ejecutar web:
- python -m vistas.web.app
  Abrir http://127.0.0.1:5000


Notas:
- Se usa SQLAlchemy como ORM para mapear clases a tablas.
- Template Method: modelos/report_template.py (PersonaReport).
- Los managers exponen insertar, buscar, listar, encontrar y borrar, tal como exige tu docente.
- CI sugerido: añadir un workflow que ejecute pytest y flake8 en cada PR.
