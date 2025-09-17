from fastapi import FastAPI
from .db.connection import Base, engine
from app.interfaces.product_routes import router as product_routes

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestión de Productos")

# Incluir rutas
app.include_router(product_routes, prefix="/api")

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de gestión de productos"}
