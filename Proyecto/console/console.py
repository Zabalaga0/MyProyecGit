# console/console.py
import requests # hace que podamos hacer solicitudes HTTP a la API REST 
from datetime import datetime, timedelta # esto nos sirve para manjerar fechas

API_URL = "http://127.0.0.1:8000/api/products/" # es la URL base de la API REST 
# metodo para mostrar el menú principal de la aplicación
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
# metodo para listar los productos obtenidos de la API REST
def list_products():
    response = requests.get(API_URL)# hace una solicitud GET a la API REST para obtener la lista de productos
    if response.status_code == 200: # si la respuesta es exitosa (código 200)  
        products = response.json()# convierte la respuesta JSON en una lista de diccionarios de productos 
        print("\n--- Lista de Productos ---") # muestra un encabezado para la lista de productos 
        for p in products:# itera sobre cada producto en la lista 
            exp = p.get("expiration_date") or "Sin fecha" # obtiene la fecha de vencimiento o "Sin fecha" si no existe 
            print( # muestra los detalles del producto en un formato legible
                f"🆔 {p['id']} | {p['name']} ({p['brand']}) | 💲{p['price']} | "
                f"Stock: {p['stock']} | Pago: {p['payment_method']} | 🗓️ Vence: {exp}"
            )
    else:# si la respuesta no es exitosa (código diferente de 200)
        print("❌ Error al obtener productos")

# -----------------------------------------------------
# metodo para agregar un nuevo producto a la API REST
def add_product():
    print("\n--- ➕ Agregar Nuevo Producto ---")
    name = input("Nombre: ") # solicita el nombre del producto al usuario
    brand = input("Marca: ") # solicita la marca del producto al usuario

    try:# intenta convertir el precio y la cantidad a los tipos adecuados
        price = float(input("Precio: "))
        stock = int(input("Cantidad: "))
    except ValueError:# si hay un error de conversión, muestra un mensaje de error y retorna
        print("❌ Ingrese valores numéricos válidos.")
        return

    payment_method = input("Método de pago (Tarjeta/Efectivo): ").capitalize()# solicita el método de pago y lo capitaliza
    if payment_method not in ["Tarjeta", "Efectivo"]:# valida el método de pago
        print("❌ Opción inválida, se asignará 'Efectivo' por defecto.")
        payment_method = "Efectivo" # asigna "Efectivo" por defecto si la opción es inválida

    expiration_date = input("Fecha de vencimiento (YYYY-MM-DD o dejar vacío): ").strip() # solicita la fecha de vencimiento y elimina espacios en blanco
    expiration_date = expiration_date if expiration_date else None # asigna None si la fecha está vacía 

    data = { # crea un diccionario con los datos del nuevo producto
        "name": name, # nombre del producto 
        "brand": brand, # marca del producto
        "price": price, # precio del producto
        "stock": stock, # cantidad en stock
        "payment_method": payment_method, # método de pago
        "expiration_date": expiration_date, # fecha de vencimiento
    }

    response = requests.post(API_URL, json=data) # hace una solicitud POST a la API REST para agregar el nuevo producto 
    if response.status_code == 200: # si la respuesta es exitosa (código 200) 
        print("✅ Producto agregado correctamente") 
    else: # si la respuesta no es exitosa (código diferente de 200) 
        print("❌ Error al agregar producto") 
        print(response.text) # muestra el texto de la respuesta para más detalles 

# -----------------------------------------------------
# metodo para actualizar un producto existente en la API REST
def update_product():
    print("\n--- ✏️  Modificar Producto ---")
    try: 
        product_id = int(input("ID del producto a modificar: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    # Obtener producto actual
    url = f"{API_URL.rstrip('/')}/{product_id}" # construye la URL para obtener el producto específico
    get_resp = requests.get(url) # hace una solicitud GET a la API REST para obtener los datos del producto 
    if get_resp.status_code != 200: # si la respuesta no es exitosa (código diferente de 200) 
        print("❌ Producto no encontrado.")
        return
    prod = get_resp.json() # convierte la respuesta JSON en un diccionario de producto

    # Mostrar datos actuales
    print(f"Producto actual: {prod['name']} ({prod['brand']}) - ${prod['price']}") 
    print("Deja en blanco si no deseas modificar un campo.")

    name = input(f"Nombre [{prod['name']}]: ") or prod['name'] # solicita el nuevo nombre del producto o mantiene el actual si se deja en blanco
    brand = input(f"Marca [{prod['brand']}]: ") or prod['brand'] # solicita la nueva marca del producto o mantiene la actual si se deja en blanco
    price = input(f"Precio [{prod['price']}]: ") or prod['price'] # solicita el nuevo precio del producto o mantiene el actual si se deja en blanco
    stock = input(f"Stock [{prod['stock']}]: ") or prod['stock'] # solicita la nueva cantidad en stock o mantiene la actual si se deja en blanco
    payment_method = input(f"Método de pago [{prod['payment_method']}]: ") or prod['payment_method'] # solicita el nuevo método de pago o mantiene el actual si se deja en blanco
    expiration_date = input(f"Fecha vencimiento [{prod.get('expiration_date','Sin fecha')}]: ") or prod.get("expiration_date") # solicita la nueva fecha de vencimiento o mantiene la actual si se deja en blanco

    try:
        price = float(price) 
        stock = int(stock)
    except ValueError:
        print("❌ Valores numéricos inválidos.")
        return
    # Construir datos actualizados
    updated = { # crea un diccionario con los datos actualizados del producto
        "name": name, # nuevo nombre del producto 
        "brand": brand, # nueva marca del producto
        "price": price, # nuevo precio del producto
        "stock": stock, # nueva cantidad en stock
        "payment_method": payment_method, # nuevo método de pago
        "expiration_date": expiration_date, # nueva fecha de vencimiento
    }

    response = requests.put(url, json=updated) # hace una solicitud PUT a la API REST para actualizar el producto 
    if response.status_code == 200: # si la respuesta es exitosa (código 200) 
        print("✅ Producto actualizado correctamente.") 
    else: # si la respuesta no es exitosa (código diferente de 200) 
        print("❌ Error al actualizar producto.")
        print(response.text)

# -----------------------------------------------------
# metodo para eliminar un producto de la API REST 
def delete_product():
    print("\n--- 💣 Eliminar Producto ---")
    try:
        product_id = int(input("ID del producto a eliminar: "))
    except ValueError:
        print("❌ ID inválido.")
        return
    url = f"{API_URL.rstrip('/')}/{product_id}" # construye la URL para eliminar el producto específico
    response = requests.delete(url) # hace una solicitud DELETE a la API REST para eliminar el producto
    if response.status_code == 200: # si la respuesta es exitosa (código 200) 
        print("🗑️ Producto eliminado correctamente.")
    else: # si la respuesta no es exitosa (código diferente de 200) 
        print("❌ Error al eliminar producto.")
        print(response.text)

# -----------------------------------------------------
# metodo para ver los productos que están próximos a vencer en los próximos 7 días
def view_expiring_products():
    print("\n--- 📆 Productos próximos a vencer (en 7 días) ---")
    response = requests.get(API_URL) # hace una solicitud GET a la API REST para obtener la lista de productos
    if response.status_code != 200: # si la respuesta no es exitosa (código diferente de 200)
        print("❌ Error al obtener productos.")
        return

    products = response.json() # convierte la respuesta JSON en una lista de diccionarios de productos
    today = datetime.today().date() # obtiene la fecha actual
    soon = today + timedelta(days=7) # calcula la fecha dentro de 7 días 

    found = False # bandera para indicar si se encontraron productos próximos a vencer
    for p in products: # itera sobre cada producto en la lista 
        exp_date = p.get("expiration_date") # obtiene la fecha de vencimiento del producto 
        if exp_date: # si el producto tiene una fecha de vencimiento
            try: # intenta convertir la fecha de vencimiento a un objeto date
                exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date() # convierte la cadena de fecha a un objeto date
                if today <= exp_date <= soon: # si la fecha de vencimiento está dentro de los próximos 7 días
                    print(f"⚠️ {p['name']} ({p['brand']}) vence el {exp_date}") # muestra el producto próximo a vencer
                    found = True # actualiza la bandera a True
            except ValueError: # si la fecha de vencimiento no tiene el formato esperado
                pass # ignora el error y continúa
    if not found: # si no se encontraron productos próximos a vencer
        print("✅ No hay productos próximos a vencer.") 

# -----------------------------------------------------
# metodo principal para ejecutar el sistema de gestión de productos
def run():
    while True: # bucle infinito para mostrar el menú y procesar las opciones del usuario
        menu() # muestra el menú principal
        option = input("Selecciona una opción📌: ").strip() # obtiene la opción seleccionada por el usuario
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

if __name__ == "__main__": # si este archivo se ejecuta como script principal
    run() # llama al método run para iniciar el sistema de gestión de productos
