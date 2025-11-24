from abc import ABC, abstractmethod
from typing import Any, List

class ReportTemplate(ABC):
    """Template Method: define el esqueleto para generar reportes."""

    def generar_reporte(self) -> str:
        partes = []
        partes.append(self._cabecera())
        partes.append(self._cuerpo())
        partes.append(self._pie())
        return "\n".join(partes)

    def _cabecera(self) -> str:
        return "=== REPORTE ==="

    @abstractmethod
    def _cuerpo(self) -> str:
        """Implementado por subclases: cómo obtener y formatear los datos"""
        pass

    def _pie(self) -> str:
        return "=== FIN DEL REPORTE ==="

class PersonaReport(ReportTemplate):
    """Implementación concreta de ReportTemplate para listar personas."""

    def __init__(self, persona_manager):
        self.manager = persona_manager

    def _cuerpo(self) -> str:
        personas = self.manager.listar()
        if not personas:
            return "(sin personas)"
        lines = [f"{{p.id}}: {{p.nombre}} ({{p.edad}})" for p in personas]
        return "\n".join(lines)
