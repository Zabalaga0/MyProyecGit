# Mi primer Proyecto en Git
Tema del Proyecto: Sistema de Gestion de Productos de una tienda 
# Estructura del proyecto
*PROYECTO
   *app
   |   *db
   |   |   *_init_.py
   |   |   *connection.py
   |   *interfaces
   |   |   *_init_.py
   |   |   *product_routes.py
   |   *managers
   |   |   *_init_.py
   |   |   *product_managers.py
   |   *models
   |   |   *_init_.py
   |   |   *product.py
   |   *schemas
   |   |   *_init_.py
   |   |   *product_schema.py
   |   *tests
   |   |   *tests.py
   |   *_init_.py
   |   *main.py
   *console
   |   *console.py
   *.gitignore
   *README.md
   *requirements.txt
   *test.db
## Raíz del Proyecto
.gitignore
Lista archivos y carpetas que Git debe ignorar (por ejemplo, __pycache__, bases de datos locales, etc.).

## README.md
Archivo de documentación principal. Explica de qué trata el proyecto, cómo instalarlo y usarlo.

## requirements.txt
Lista de dependencias (librerías) necesarias para que el proyecto funcione.

## test.db
Archivo de base de datos SQLite usado para pruebas o desarrollo.

# Carpeta app
Contiene el código principal de la aplicación.

## Subcarpeta db
### init.py
Indica que la carpeta es un módulo de Python.
### connection.py
Aquí se gestiona la conexión a la base de datos (crear, abrir, cerrar conexiones, etc.).
## Subcarpeta interfaces
### init.py
Indica que la carpeta es un módulo.
### product_routes.py
Define las rutas/endpoints de la API relacionados con productos (por ejemplo, /products, /products/{id}).
## Subcarpeta managers
### init.py
### product_managers.py
Contiene la lógica de negocio para productos. Aquí se decide qué hacer al crear, leer, actualizar o borrar un producto. Interactúa con la base de datos y aplica reglas de negocio.
## Subcarpeta models
### init.py
### product.py
Define cómo es la estructura de un producto en la base de datos (modelo ORM: Object Relational Mapper).
## Subcarpeta schemas
### init.py
### product_schema.py
Define los esquemas de validación de datos para productos (por ejemplo, qué datos debe tener un producto al crearse o actualizarse). Suele usarse con Pydantic o Marshmallow.
## Subcarpeta tests
### tests.py
Pruebas automáticas para verificar que la aplicación funciona como se espera.
# Otros archivos en app
## init.py
Hace que la carpeta app sea un paquete de Python.
## main.py
Es el punto de entrada de la aplicación. Aquí se inicializa la app y se registran rutas/endpoints.
Carpeta console
## console.py
Archivo para ejecutar comandos desde la terminal (quizás para tareas administrativas, cargar datos, etc.).
# ¿Cómo funciona todo junto?
- main.py inicializa la aplicación.
- Cuando llega una petición (por ejemplo, un usuario consulta /products):
    - product_routes.py define qué hacer con esa petición.
    - Llama a la lógica de negocio en product_managers.py.
    - Ese manager consulta o modifica los datos en la base usando product.py y la conexión de connection.py.
    - Los datos que entran/salen se validan con product_schema.py.
- tests.py comprueba que todo esto funcione correctamente.
- console.py sirve para tareas manuales/administrativas desde la terminal.