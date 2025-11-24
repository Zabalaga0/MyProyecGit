from typing import List, Optional, Any
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from modelos.producto import Producto
from modelos.base import Base
from datetime import date, timedelta

class ProductoManager:
    def __init__(self, db_url: str = "sqlite:///productos.db", session: Optional[Session] = None):
        if session is not None:
            self.session = session
            self._owns_session = False
        else:
            engine = create_engine(db_url, echo=False, future=True)
            Base.metadata.create_all(engine)
            SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
            self.session = SessionLocal()
            self._owns_session = True

    def insertar(self, nombre: str, precio: float, cantidad: int = 0, descripcion: str = None, fecha_vencimiento: Optional[date] = None) -> Producto:
        p = Producto(nombre=nombre, precio=precio, cantidad=cantidad, descripcion=descripcion, fecha_vencimiento=fecha_vencimiento)
        self.session.add(p)
        self.session.commit()
        self.session.refresh(p)
        return p

    def buscar(self, producto_id: int) -> Optional[Producto]:
        return self.session.get(Producto, producto_id)

    def listar(self) -> List[Producto]:
        return self.session.query(Producto).all()

    def modificar(self, producto_id: int, **campos) -> Optional[Producto]:
        p = self.buscar(producto_id)
        if not p:
            return None
        for k, v in campos.items():
            if hasattr(Producto, k):
                setattr(p, k, v)
        self.session.commit()
        self.session.refresh(p)
        return p

    def eliminar(self, producto_id: int) -> bool:
        p = self.buscar(producto_id)
        if not p:
            return False
        self.session.delete(p)
        self.session.commit()
        return True

    def encontrar(self, **filtros: Any) -> List[Producto]:
        q = self.session.query(Producto)
        for attr, val in filtros.items():
            if hasattr(Producto, attr):
                q = q.filter(getattr(Producto, attr) == val)
        return q.all()

    def proximos_a_vencer(self, dias: int = 30) -> List[Producto]:
        hoy = date.today()
        limite = hoy + timedelta(days=dias)
        return self.session.query(Producto)\
            .filter(Producto.fecha_vencimiento != None)\
            .filter(Producto.fecha_vencimiento >= hoy)\
            .filter(Producto.fecha_vencimiento <= limite).all()

    def cerrar(self):
        if self._owns_session:
            self.session.close()