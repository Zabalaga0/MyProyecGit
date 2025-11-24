import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from managers.producto_manager import ProductoManager
from modelos.producto import Producto
from datetime import date, timedelta

@pytest.fixture
def manager_in_memory():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    m = ProductoManager(session=session)
    yield m
    m.cerrar()

def test_insertar_listar(manager_in_memory):
    p = manager_in_memory.insertar("Leche", 1.5, cantidad=10)
    assert isinstance(p, Producto)
    lista = manager_in_memory.listar()
    assert len(lista) == 1
    assert lista[0].nombre == "Leche"

def test_modificar_eliminar(manager_in_memory):
    p = manager_in_memory.insertar("Queso", 2.5, cantidad=3)
    manager_in_memory.modificar(p.id, precio=3.0, cantidad=5)
    p2 = manager_in_memory.buscar(p.id)
    assert p2.precio == 3.0
    assert manager_in_memory.eliminar(p.id)
    assert manager_in_memory.buscar(p.id) is None

def test_proximos_a_vencer(manager_in_memory):
    hoy = date.today()
    fv = hoy + timedelta(days=5)
    manager_in_memory.insertar("Yogurt", 0.9, cantidad=6, fecha_vencimiento=fv)
    lista = manager_in_memory.proximos_a_vencer(dias=7)
    assert len(lista) == 1