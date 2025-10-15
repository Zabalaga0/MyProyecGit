# console/console.py
import requests

API_URL = "http://127.0.0.1:8000/api/products/"

def menu():
    print("\n--- Sistema de Gestión de Productos ---")
    print("1. 📝 Listar productos")
    print("2. 🛒 Agregar producto")
    print("3. 💣 Eliminar producto")
    print("4. 🗿 Salir")

def list_products():
    response = requests.get(API_URL)
    if response.status_code == 200:
        products = response.json()
        print("\n--- Lista de Productos ---")
        for p in products:
            print(
                f"{p['id']} - {p['name']} ({p['brand']}) - "
                f"${p['price']} - Stock: {p['stock']} - Pago: {p['payment_method']}"
            )
    else:
        print("Error al obtener productos")

def add_product():
    print("\n--- Agregar Nuevo Producto ---")
    name = input("Nombre: ")
    brand = input("Marca: ")

    try:
        price = float(input("Precio: "))
        stock = int(input("Cantidad: "))
    except ValueError:
        print("❌Ingrese un número válido para precio y stock‼️")
        return

    # 💳 Nuevo paso: elegir método de pago
    payment_method = input("Método de pago (Tarjeta/Efectivo): ").capitalize()
    if payment_method not in ["Tarjeta", "Efectivo"]:
        print("❌ Opción inválida, se asignará 'Efectivo' por defecto.")
        payment_method = "Efectivo"

    data = {
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "payment_method": payment_method,
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        print("✅ Producto agregado correctamente")
    else:
        print("❌ Error al agregar producto")
        print(response.text)
