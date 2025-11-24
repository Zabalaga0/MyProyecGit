from typing import List, Optional, Any
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from modelos.persona import Persona
from modelos.base import Base

class PersonaManager:
    """
    Manager responsable de operaciones CRUD para Persona.
    Instanciar con una session (para tests) o con db_url (por defecto sqlite file).
    """

    def __init__(self, db_url: str = "sqlite:///personas.db", session: Optional[Session] = None):
        if session is not None:
            self.session = session
            self._owns_session = False
        else:
            engine = create_engine(db_url, echo=False, future=True)
            Base.metadata.create_all(engine)
            SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
            self.session = SessionLocal()
            self._owns_session = True

    def insertar(self, nombre: str, edad: int) -> Persona:
        persona = Persona(nombre=nombre, edad=edad)
        self.session.add(persona)
        self.session.commit()
        self.session.refresh(persona)
        return persona

    def buscar(self, persona_id: int) -> Optional[Persona]:
        return self.session.get(Persona, persona_id)

    def listar(self) -> List[Persona]:
        return self.session.query(Persona).all()

    def encontrar(self, **filtros: Any) -> List[Persona]:
        q = self.session.query(Persona)
        for attr, val in filtros.items():
            if hasattr(Persona, attr):
                q = q.filter(getattr(Persona, attr) == val)
        return q.all()

    def borrar(self, persona_id: int) -> bool:
        p = self.buscar(persona_id)
        if not p:
            return False
        self.session.delete(p)
        self.session.commit()
        return True

    def cerrar(self):
        if self._owns_session:
            self.session.close()
