from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos (aquí un ejemplo con SQLite)
DATABASE_URL = "sqlite:///./test.db"

# Crear el motor de conexión
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Necesario solo para SQLite
)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia que retorna la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
