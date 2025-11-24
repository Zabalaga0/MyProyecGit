from flask import Flask, render_template_string, request, redirect, url_for
from managers.producto_manager import ProductoManager
from datetime import datetime

app = Flask(__name__)

LIST_HTML = """
<!doctype html>
<title>Productos</title>
<h1>Productos</h1>
<a href="{{ url_for('add') }}">Agregar nuevo</a> | <a href="{{ url_for('expiring') }}">Próximos a vencer</a>
<ul>
  {% for p in productos %}
    <li>{{ p.id }} - {{ p.nombre }} ({{ p.cantidad }}) - {{ p.precio }} - Vence: {{ p.fecha_vencimiento }}
        [<a href="{{ url_for('edit', producto_id=p.id) }}">editar</a>]
        [<a href="{{ url_for('delete', producto_id=p.id) }}">eliminar</a>]
    </li>
  {% endfor %}
</ul>
"""

FORM_HTML = """
<!doctype html>
<title>{{ titulo }}</title>
<h1>{{ titulo }}</h1>
<form method="post">
  Nombre: <input name="nombre" value="{{ producto.nombre if producto else '' }}"><br>
  Descripcion: <input name="descripcion" value="{{ producto.descripcion if producto else '' }}"><br>
  Precio: <input name="precio" value="{{ producto.precio if producto else '' }}" type="number" step="0.01"><br>
  Cantidad: <input name="cantidad" value="{{ producto.cantidad if producto else '' }}" type="number"><br>
  Fecha de vencimiento: <input name="fecha_vencimiento" value="{{ producto.fecha_vencimiento if producto and producto.fecha_vencimiento else '' }}" placeholder="YYYY-MM-DD"><br>
  <button type="submit">Guardar</button>
</form>
<a href="{{ url_for('index') }}">Volver</a>
"""

@app.route("/")
def index():
    m = ProductoManager()
    try:
        productos = m.listar()
        return render_template_string(LIST_HTML, productos=productos)
    finally:
        m.cerrar()

@app.route("/add", methods=["GET", "POST"])
def add():
    m = ProductoManager()
    try:
        if request.method == "POST":
            nombre = request.form["nombre"]
            descripcion = request.form.get("descripcion") or None
            precio = float(request.form.get("precio") or 0)
            cantidad = int(request.form.get("cantidad") or 0)
            fv = request.form.get("fecha_vencimiento") or None
            fv_date = datetime.strptime(fv, "%Y-%m-%d").date() if fv else None
            m.insertar(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, fecha_vencimiento=fv_date)
            return redirect(url_for("index"))
        return render_template_string(FORM_HTML, titulo="Agregar producto", producto=None)
    finally:
        m.cerrar()

@app.route("/edit/<int:producto_id>", methods=["GET", "POST"])
def edit(producto_id):
    m = ProductoManager()
    try:
        p = m.buscar(producto_id)
        if not p:
            return "No encontrado", 404
        if request.method == "POST":
            nombre = request.form["nombre"]
            descripcion = request.form.get("descripcion") or None
            precio = float(request.form.get("precio") or 0)
            cantidad = int(request.form.get("cantidad") or 0)
            fv = request.form.get("fecha_vencimiento") or None
            fv_date = datetime.strptime(fv, "%Y-%m-%d").date() if fv else None
            m.modificar(producto_id, nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, fecha_vencimiento=fv_date)
            return redirect(url_for("index"))
        return render_template_string(FORM_HTML, titulo="Editar producto", producto=p)
    finally:
        m.cerrar()

@app.route("/delete/<int:producto_id>")
def delete(producto_id):
    m = ProductoManager()
    try:
        m.eliminar(producto_id)
        return redirect(url_for("index"))
    finally:
        m.cerrar()

@app.route("/expiring")
def expiring():
    dias = int(request.args.get("dias", 30))
    m = ProductoManager()
    try:
        lista = m.proximos_a_vencer(dias=dias)
        return render_template_string("""
            <h1>Productos próximos a vencer ({{ dias }} días)</h1>
            <ul>
            {% for p in lista %}
              <li>{{ p.id }} - {{ p.nombre }} - Vence: {{ p.fecha_vencimiento }} (Cant: {{ p.cantidad }})</li>
            {% endfor %}
            </ul>
            <a href="{{ url_for('index') }}">Volver</a>
        """, lista=lista, dias=dias)
    finally:
        m.cerrar()

if __name__ == "__main__":
    app.run(debug=True, port=5000)