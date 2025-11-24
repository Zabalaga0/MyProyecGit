from flask import Flask, render_template_string, request, redirect, url_for
from managers.persona_manager import PersonaManager

app = Flask(__name__)

LIST_HTML = """
<!doctype html>
<title>Personas</title>
<h1>Personas</h1>
<ul>
  {% for p in personas %}
    <li>{{ p.id }} - {{ p.nombre }} ({{ p.edad }})</li>
  {% endfor %}
</ul>

<h2>Agregar</h2>
<form method="post" action="{{ url_for('add') }}">
  Nombre: <input name="nombre"><br>
  Edad: <input name="edad" type="number"><br>
  <button type="submit">Agregar</button>
</form>
"""

@app.route("/", methods=["GET"])
def index():
    manager = PersonaManager()
    try:
        personas = manager.listar()
        return render_template_string(LIST_HTML, personas=personas)
    finally:
        manager.cerrar()

@app.route("/add", methods=["POST"])
def add():
    nombre = request.form["nombre"]
    edad = int(request.form["edad"])
    manager = PersonaManager()
    try:
        manager.insertar(nombre, edad)
    finally:
        manager.cerrar()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
