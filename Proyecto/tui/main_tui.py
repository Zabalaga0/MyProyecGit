# tui/main_tui.py
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, Input, DataTable, Label
)
import requests
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:8000/api/products/"


# ╭───────────────────────────────────────────────────────────────╮
# │                       APP PRINCIPAL                           │
# ╰───────────────────────────────────────────────────────────────╯
class ProductTUI(App):
    TITLE = "🏪 Sistema de Gestión de Productos (TUI)"
    SUB_TITLE = "Powered by Textual + FastAPI"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("📦 SISTEMA DE PRODUCTOS", id="title"),
            Horizontal(
                Button("📋 Listar", id="list", variant="primary"),
                Button("🛒 Agregar", id="add", variant="success"),
                Button("✏️ Modificar", id="edit", variant="primary"),
                Button("💣 Eliminar", id="delete", variant="error"),
                Button("📆 Próximos a vencer", id="near", variant="warning"),
                Button("🚪 Salir", id="exit", variant="default"),
                id="menu_buttons"
            ),
            DataTable(id="table"),
            id="main_container"
        )
        yield Footer()

    def on_mount(self):
        table = self.query_one("#table", DataTable)
        table.add_columns("ID", "Nombre", "Marca", "Precio", "Stock", "Pago", "Vencimiento")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "list":
                self.list_products()
            case "add":
                self.push_screen(AddProductForm(main_app=self))
            case "edit":
                self.push_screen(EditProductForm(main_app=self))
            case "delete":
                self.push_screen(DeleteProductConfirm(main_app=self))
            case "near":
                self.products_near_expiration()
            case "exit":
                self.exit()

    def list_products(self):
        table = self.query_one("#table", DataTable)
        table.clear()
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                products = response.json()
                for p in products:
                    table.add_row(
                        str(p["id"]),
                        p["name"],
                        p["brand"],
                        f"${p['price']:.2f}",
                        str(p["stock"]),
                        p["payment_method"],
                        p.get("expiration_date", "—")
                    )
                self.notify("✅ Productos cargados correctamente", severity="information")
            else:
                self.notify("❌ Error al obtener productos", severity="error")
        except Exception as e:
            self.notify(f"⚠️ Error: {e}", severity="error")

    def products_near_expiration(self):
        try:
            response = requests.get(API_URL)
            if response.status_code != 200:
                raise Exception("Error al obtener productos")

            products = response.json()
            today = datetime.today().date()
            limit = today + timedelta(days=7)
            near = [
                p for p in products
                if p.get("expiration_date") and
                datetime.strptime(p["expiration_date"], "%Y-%m-%d").date() <= limit
            ]

            table = self.query_one("#table", DataTable)
            table.clear()
            for p in near:
                table.add_row(
                    str(p["id"]), p["name"], p["brand"], f"${p['price']:.2f}",
                    str(p["stock"]), p["payment_method"], p["expiration_date"]
                )

            if not near:
                self.notify("😎 No hay productos próximos a vencer", severity="information")
            else:
                self.notify("📆 Mostrando productos que vencen en los próximos 7 días", severity="success")

        except Exception as e:
            self.notify(f"❌ Error: {e}", severity="error")


# ╭───────────────────────────────────────────────────────────────╮
# │                 FORMULARIO: AGREGAR PRODUCTO                  │
# ╰───────────────────────────────────────────────────────────────╯
class AddProductForm(Screen):
    def __init__(self, main_app: ProductTUI):
        super().__init__()
        self.main_app = main_app

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("🧾 Agregar nuevo producto"),
            Input(placeholder="Nombre", id="name"),
            Input(placeholder="Marca", id="brand"),
            Input(placeholder="Precio", id="price"),
            Input(placeholder="Stock", id="stock"),
            Input(placeholder="Método de pago (Efectivo/Tarjeta)", id="payment_method"),
            Input(placeholder="Fecha de vencimiento (YYYY-MM-DD)", id="expiration_date"),
            Horizontal(
                Button("💾 Guardar", id="save", variant="success"),
                Button("↩️ Cancelar", id="cancel", variant="default")
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save":
            try:
                data = {
                    "name": self.query_one("#name", Input).value,
                    "brand": self.query_one("#brand", Input).value,
                    "price": float(self.query_one("#price", Input).value),
                    "stock": int(self.query_one("#stock", Input).value),
                    "payment_method": self.query_one("#payment_method", Input).value.capitalize(),
                    "expiration_date": self.query_one("#expiration_date", Input).value
                }
                res = requests.post(API_URL, json=data)
                if res.status_code == 200:
                    self.main_app.notify("✅ Producto agregado correctamente", severity="success")
                    self.main_app.list_products()
                    self.app.pop_screen()
                else:
                    self.main_app.notify("❌ Error al agregar producto", severity="error")
            except Exception as e:
                self.main_app.notify(f"⚠️ Error: {e}", severity="error")
        elif event.button.id == "cancel":
            self.app.pop_screen()


# ╭───────────────────────────────────────────────────────────────╮
# │                 FORMULARIO: EDITAR PRODUCTO                   │
# ╰───────────────────────────────────────────────────────────────╯
class EditProductForm(Screen):
    def __init__(self, main_app: ProductTUI):
        super().__init__()
        self.main_app = main_app

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("✏️ Editar producto existente"),
            Input(placeholder="ID del producto a editar", id="id"),
            Input(placeholder="Nuevo nombre (vacío = mantener)", id="name"),
            Input(placeholder="Nueva marca", id="brand"),
            Input(placeholder="Nuevo precio", id="price"),
            Input(placeholder="Nuevo stock", id="stock"),
            Input(placeholder="Nuevo método de pago", id="payment_method"),
            Input(placeholder="Nueva fecha de vencimiento (YYYY-MM-DD)", id="expiration_date"),
            Horizontal(
                Button("💾 Guardar cambios", id="save", variant="success"),
                Button("↩️ Cancelar", id="cancel", variant="default")
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save":
            try:
                pid = self.query_one("#id", Input).value
                if not pid:
                    self.main_app.notify("⚠️ Debes ingresar un ID válido", severity="warning")
                    return

                update_data = {}
                for field in ["name", "brand", "price", "stock", "payment_method", "expiration_date"]:
                    val = self.query_one(f"#{field}", Input).value
                    if val:
                        update_data[field] = val

                res = requests.put(f"{API_URL}{pid}", json=update_data)
                if res.status_code == 200:
                    self.main_app.notify("✅ Producto modificado correctamente", severity="success")
                    self.main_app.list_products()
                    self.app.pop_screen()
                else:
                    self.main_app.notify("❌ Error al modificar producto", severity="error")
            except Exception as e:
                self.main_app.notify(f"⚠️ Error: {e}", severity="error")
        elif event.button.id == "cancel":
            self.app.pop_screen()


# ╭───────────────────────────────────────────────────────────────╮
# │                 CONFIRMACIÓN DE ELIMINAR                      │
# ╰───────────────────────────────────────────────────────────────╯
class DeleteProductConfirm(Screen):
    def __init__(self, main_app: ProductTUI):
        super().__init__()
        self.main_app = main_app

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("💣 Eliminar producto"),
            Input(placeholder="ID del producto a eliminar", id="id"),
            Horizontal(
                Button("🗑️ Confirmar eliminación", id="confirm", variant="error"),
                Button("↩️ Cancelar", id="cancel", variant="default")
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "confirm":
            try:
                pid = int(self.query_one("#id", Input).value)
                res = requests.delete(f"{API_URL}{pid}")
                if res.status_code == 200:
                    self.main_app.notify("✅ Producto eliminado correctamente", severity="success")
                    self.main_app.list_products()
                else:
                    self.main_app.notify("⚠️ Error al eliminar producto", severity="error")
                self.app.pop_screen()
            except Exception as e:
                self.main_app.notify(f"⚠️ Error: {e}", severity="error")
        elif event.button.id == "cancel":
            self.app.pop_screen()


# ╭───────────────────────────────────────────────────────────────╮
# │                        EJECUCIÓN                              │
# ╰───────────────────────────────────────────────────────────────╯
if __name__ == "__main__":
    app = ProductTUI()
    app.run()
