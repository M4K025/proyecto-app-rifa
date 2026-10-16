from dataclasses import dataclass, field
from datetime import datetime
from .enums import EstadoPago

@dataclass
class Pago:
    id: int
    compra_id: int
    monto: float
    referencia: str = ''
    estado: EstadoPago = EstadoPago.PENDIENTE
    fecha: datetime = field(default_factory=datetime.now)

    def aprobar(self) -> None:
        self.estado = EstadoPago.APROBADO

    def rechazar(self) -> None:
        self.estado = EstadoPago.RECHAZADO
