import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from managers.persona_manager import PersonaManager
from modelos.persona import Persona

@pytest.fixture
def in_memory_manager():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()
    manager = PersonaManager(session=session)
    yield manager
    manager.cerrar()


def test_insertar_y_listar(in_memory_manager):
    p = in_memory_manager.insertar("Ana", 28)
    assert isinstance(p, Persona)
    lista = in_memory_manager.listar()
    assert len(lista) == 1
    assert lista[0].nombre == "Ana"
    assert lista[0].edad == 28


def test_buscar_encontrar(in_memory_manager):
    p = in_memory_manager.insertar("Luis", 30)
    encontrado = in_memory_manager.buscar(p.id)
    assert encontrado.nombre == "Luis"
    matches = in_memory_manager.encontrar(nombre="Luis")
    assert len(matches) == 1
