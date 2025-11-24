from sqlalchemy import Column, Integer, String
from .base import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Persona id={self.id} nombre={self.nombre} edad={self.edad}>"