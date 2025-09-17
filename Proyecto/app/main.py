from fastapi import FastAPI
from app.db.connection import Base, engine
from app.interfaces import product_routes

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestión de Productos")

# Incluir rutas
app.include_router(product_routes.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de gestión de productos"}
