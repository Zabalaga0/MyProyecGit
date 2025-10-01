# Mi Proyecto con FastAPI

## Explicación de los comandos para la compilación y ejecución del proyecto

### 1. Clonar el repositorio
```powershell
git clone https://github.com/Zabalaga0/MyProyecGit.git
```
**¿Qué es y para qué sirve?**  
Este comando descarga una copia del repositorio remoto de GitHub a tu computadora local. Así obtienes todo el código fuente y archivos del proyecto para trabajar en él.

---

### 2. Entrar al repositorio
```powershell
cd MyProyecGit
```
**¿Qué es y para qué sirve?**  
Este comando te permite ingresar a la carpeta del repositorio recién descargado, para poder ejecutar los siguientes comandos dentro de esa carpeta.

---

### 3. Crear un entorno virtual
```powershell
python -m venv venv
```
**¿Qué es y para qué sirve?**  
Este comando crea un entorno virtual llamado `venv` en la carpeta actual. Un entorno virtual te permite instalar dependencias específicas del proyecto sin afectar otras configuraciones de Python en tu computadora.

---

### 4. Activar el entorno virtual

**Para Windows:**
```powershell
venv\Scripts\activate
```
**Para Linux:**
```powershell
source venv/bin/activate
```
**¿Qué es y para qué sirve?**  
Estos comandos activan el entorno virtual que creaste. Así, los paquetes que instales o uses estarán aislados y pertenecen solo a este proyecto.

---

### 5. Verificar la versión de Python
```powershell
python --version
```
**¿Qué es y para qué sirve?**  
Muestra la versión de Python que está activa en tu entorno actual. Esto es útil para asegurarte de que estás utilizando la versión correcta requerida por el proyecto.

---

### 6. Entrar al directorio del proyecto
```powershell
cd Proyecto
```
**¿Qué es y para qué sirve?**  
Este comando te mueve a la carpeta llamada "Proyecto" dentro del repositorio, donde probablemente se encuentra el código principal de la aplicación.

---

### 7. Ejecutar el servidor FastAPI con Uvicorn
```powershell
uvicorn app.main:app --reload
```
**¿Qué es y para qué sirve?**  
Este comando inicia el servidor de desarrollo de FastAPI usando Uvicorn.  
- `app.main:app` le dice a Uvicorn dónde está la aplicación FastAPI (en el archivo `main.py` dentro del módulo `app`).
- `--reload` permite que el servidor se reinicie automáticamente cuando detecta cambios en el código, facilitando el desarrollo.

---

### 8. Acceder a la documentación interactiva

Visita el enlace:

**http://127.0.0.1:8000/doc**

**¿Qué es y para qué sirve?**  
Este enlace abre la documentación interactiva de tu API generada automáticamente por FastAPI. Aquí puedes probar los endpoints de la API desde el navegador.

---
