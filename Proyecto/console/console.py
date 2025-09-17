import requests

API_URL = "http://127.0.0.1:8000/products"

def menu():
    print("\n--- Sistema de Gestión de Productos ---")
    print("1. Listar productos")
    print("2. Agregar producto")
    print("3. Eliminar producto")
    print("4. Salir")

def list_products():
    response = requests.get(API_URL)
    if response.status_code == 200:
        products = response.json()
        for p in products:
            print(f"{p['id']} - {p['name']} ({p['brand']}) - ${p['price']} - Stock: {p['stock']}")
    else:
        print("Error al obtener productos")

def add_product():
    name = input("Nombre: ")
    brand = input("Marca: ")
    price = float(input("Precio: "))
    stock = int(input("Stock: "))
    data = {"name": name, "brand": brand, "price": price, "stock": stock}
    response = requests.post(API_URL, json=data)
    print("Producto agregado" if response.status_code == 200 else "Error al agregar producto")

def delete_product():
    product_id = input("ID del producto a eliminar: ")
    response = requests.delete(f"{API_URL}/{product_id}")
    print("Producto eliminado" if response.status_code == 200 else "Error al eliminar producto")

def run():
    while True:
        menu()
        option = input("Selecciona una opción: ")
        if option == "1":
            list_products()
        elif option == "2":
            add_product()
        elif option == "3":
            delete_product()
        elif option == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    run()
