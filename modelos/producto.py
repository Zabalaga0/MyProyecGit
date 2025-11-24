from sqlalchemy import Column, Integer, String, Float, Date
from .base import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False, default=0.0)
    cantidad = Column(Integer, nullable=False, default=0)
    fecha_vencimiento = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Producto id={self.id} nombre={self.nombre} precio={self.precio} cant={self.cantidad} venc={self.fecha_vencimiento}>"
