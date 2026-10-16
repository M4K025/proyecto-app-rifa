from dataclasses import dataclass, field
from datetime import datetime
from .enums import TipoReporte


@dataclass
class Reporte:
    id: int
    rifa_id: int
    tipo: TipoReporte = TipoReporte.RECAUDACION
    fecha_generacion: datetime = field(default_factory=datetime.now)
    contenido: str = ""

    def generar(self, resumen: str) -> None:
        self.contenido = resumen
        self.fecha_generacion = datetime.now()

    def exportar(self) -> str:
        return f"[{self.tipo.value}] Rifa {self.rifa_id} {self.fecha_generacion:%Y-%m-%d %H:%M}\n{self.contenido}"


@dataclass
class Comprobante:
    """Comprobante de Compra (XMI), distinto de Reporte administrativo."""
    id: int
    compra_id: int
    codigo_qr: str = ""
    fecha_emision: datetime = field(default_factory=datetime.now)

    def enviar_por_correo(self, destino: str) -> str:
        return f"Comprobante {self.id} compra {self.compra_id} enviado a {destino}"
