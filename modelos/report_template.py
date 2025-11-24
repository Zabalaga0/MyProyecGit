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
        pass

    def _pie(self) -> str:
        return "=== FIN DEL REPORTE ==="

class ProductoReport(ReportTemplate):
    def __init__(self, producto_manager):
        self.manager = producto_manager

    def _cuerpo(self) -> str:
        productos = self.manager.listar()
        if not productos:
            return "(sin productos)"
        lines = [f"{p.id}: {p.nombre} ({p.cantidad}) - {p.precio}" for p in productos]
        return "\n".join(lines)