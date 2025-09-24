import requests # importa la libreria requests para hacer solicitudes HTTP
# requests es una libreria que permite hacer solicitudes HTTP de manera sencilla
# es decir , permite enviar y recibir datos a traves de la web
API_URL = "http://127.0.0.1:8000/api/products/" # URL de la API donde se gestionan los productos
# en este caso es una API local que corre en el puerto 8000

def menu():# funcion llamada menu 
    print("\n--- Sistema de Gestión de Productos ---")# imprime en pantalla el menu
    print("1. 📝 Listar productos") # imprime en pantalla las posibles opciones del menu
    print("2. 🛒 Agregar producto")
    print("3. 💣 Eliminar producto")
    print("4. 🗿 Salir")

def list_products(): # funcion llamada list_products
    response = requests.get(API_URL) # realiza una solicitud GET a la API para obtener la lista de productos
    if response.status_code == 200: # si la respuesta es exitosa (código 200)
        products = response.json() # convierte la respuesta JSON en una lista de productos
        print("\n--- Lista de Productos ---") # imprime en pantalla la lista de productos
        for p in products: # itera sobre cada producto en la lista
            print(f"{p['id']} - {p['name']} ({p['brand']}) - ${p['price']} - Stock: {p['stock']}") # imprime en pantalla los detalles de cada producto
    else: # si la respuesta no es exitosa
        print("Error al obtener productos")

def add_product():
    print("\n--- Agregar Nuevo Producto ---") 
    name = input("Nombre: ")
    brand = input("Marca: ")
    try:
        price = float(input("Precio: "))
        stock = int(input("Cantidad: "))
    except ValueError:
        print("❌Ingrese un numero valido para precio y stock‼️")
        return  # Detiene la ejecucion de la funcion si hay un error de conversion
     # solicita al usuario los detalles del nuevo producto
    data = {"name": name, "brand": brand, "price": price, "stock": stock} # crea un diccionario con los detalles del producto
    response = requests.post(API_URL, json=data) # realiza una solicitud POST a la API para agregar el nuevo producto
    if response.status_code == 200:
        print("Producto agregado")
    else:
        print("Error al agregar producto")
        print(response.text)  # Muestra el mensaje de error detallado

def delete_product():
    product_id = input("ID del producto a eliminar: ")
    try:
        product_id = int(product_id)
    except ValueError:
        print("❌ El ID debe ser un número entero")
        return
    url = f"{API_URL.rstrip('/')}/{product_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Producto eliminado")
    else:
        print("Error al eliminar producto")
        print(response.text)

def run():
    while True:
        menu()
        option = input("Selecciona una opción📌: ")
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
