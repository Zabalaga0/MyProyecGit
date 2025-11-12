# console/console.py
import requests
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:8000/api/products/"

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

# -----------------------------------------------------
def list_products():
    response = requests.get(API_URL)
    if response.status_code == 200:
        products = response.json()
        print("\n--- Lista de Productos ---")
        for p in products:
            exp = p.get("expiration_date") or "Sin fecha"
            print(
                f"🆔 {p['id']} | {p['name']} ({p['brand']}) | 💲{p['price']} | "
                f"Stock: {p['stock']} | Pago: {p['payment_method']} | 🗓️ Vence: {exp}"
            )
    else:
        print("❌ Error al obtener productos")

# -----------------------------------------------------
def add_product():
    print("\n--- ➕ Agregar Nuevo Producto ---")
    name = input("Nombre: ")
    brand = input("Marca: ")

    try:
        price = float(input("Precio: "))
        stock = int(input("Cantidad: "))
    except ValueError:
        print("❌ Ingrese valores numéricos válidos.")
        return

    payment_method = input("Método de pago (Tarjeta/Efectivo): ").capitalize()
    if payment_method not in ["Tarjeta", "Efectivo"]:
        print("❌ Opción inválida, se asignará 'Efectivo' por defecto.")
        payment_method = "Efectivo"

    expiration_date = input("Fecha de vencimiento (YYYY-MM-DD o dejar vacío): ").strip()
    expiration_date = expiration_date if expiration_date else None

    data = {
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "payment_method": payment_method,
        "expiration_date": expiration_date,
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        print("✅ Producto agregado correctamente")
    else:
        print("❌ Error al agregar producto")
        print(response.text)

# -----------------------------------------------------
def update_product():
    print("\n--- ✏️  Modificar Producto ---")
    try:
        product_id = int(input("ID del producto a modificar: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    # Obtener producto actual
    url = f"{API_URL.rstrip('/')}/{product_id}"
    get_resp = requests.get(url)
    if get_resp.status_code != 200:
        print("❌ Producto no encontrado.")
        return
    prod = get_resp.json()

    # Mostrar datos actuales
    print(f"Producto actual: {prod['name']} ({prod['brand']}) - ${prod['price']}")
    print("Deja en blanco si no deseas modificar un campo.")

    name = input(f"Nombre [{prod['name']}]: ") or prod['name']
    brand = input(f"Marca [{prod['brand']}]: ") or prod['brand']
    price = input(f"Precio [{prod['price']}]: ") or prod['price']
    stock = input(f"Stock [{prod['stock']}]: ") or prod['stock']
    payment_method = input(f"Método de pago [{prod['payment_method']}]: ") or prod['payment_method']
    expiration_date = input(f"Fecha vencimiento [{prod.get('expiration_date','Sin fecha')}]: ") or prod.get("expiration_date")

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        print("❌ Valores numéricos inválidos.")
        return

    updated = {
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "payment_method": payment_method,
        "expiration_date": expiration_date,
    }

    response = requests.put(url, json=updated)
    if response.status_code == 200:
        print("✅ Producto actualizado correctamente.")
    else:
        print("❌ Error al actualizar producto.")
        print(response.text)

# -----------------------------------------------------
def delete_product():
    print("\n--- 💣 Eliminar Producto ---")
    try:
        product_id = int(input("ID del producto a eliminar: "))
    except ValueError:
        print("❌ ID inválido.")
        return
    url = f"{API_URL.rstrip('/')}/{product_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("🗑️ Producto eliminado correctamente.")
    else:
        print("❌ Error al eliminar producto.")
        print(response.text)

# -----------------------------------------------------
def view_expiring_products():
    print("\n--- 📆 Productos próximos a vencer (en 7 días) ---")
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("❌ Error al obtener productos.")
        return

    products = response.json()
    today = datetime.today().date()
    soon = today + timedelta(days=7)

    found = False
    for p in products:
        exp_date = p.get("expiration_date")
        if exp_date:
            try:
                exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                if today <= exp_date <= soon:
                    print(f"⚠️ {p['name']} ({p['brand']}) vence el {exp_date}")
                    found = True
            except ValueError:
                pass
    if not found:
        print("✅ No hay productos próximos a vencer.")

# -----------------------------------------------------
def run():
    while True:
        menu()
        option = input("Selecciona una opción📌: ").strip()
        if option == "1":
            list_products()
        elif option == "2":
            add_product()
        elif option == "3":
            update_product()
        elif option == "4":
            delete_product()
        elif option == "5":
            view_expiring_products()
        elif option == "6":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    run()
