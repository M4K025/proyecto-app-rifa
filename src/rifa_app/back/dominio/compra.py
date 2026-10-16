from dataclasses import dataclass, field
from datetime import datetime
from .enums import EstadoBoleto, EstadoCompra, MetodoPago
from .boleto import Boleto


@dataclass
class Compra:
    """Una compra agrupa 1..N boletos (relación incluye del XMI)."""
    id: int
    usuario_id: int
    boletos: list[Boleto] = field(default_factory=list)
    metodo_pago: MetodoPago = MetodoPago.EFECTIVO
    estado: EstadoCompra = EstadoCompra.PENDIENTE
    fecha: datetime = field(default_factory=datetime.now)

    def calcular_total(self) -> float:
        return sum(b.precio for b in self.boletos)

    @property
    def total(self) -> float:
        return self.calcular_total()

    def confirmar(self) -> None:
        if not self.boletos:
            raise ValueError("compra sin boletos")
        for b in self.boletos:
            b.marcar_vendido()
        self.estado = EstadoCompra.CONFIRMADA

    def anular(self) -> None:
        for b in self.boletos:
            if b.estado == EstadoBoleto.APARTADO:
                b.liberar()
        self.estado = EstadoCompra.ANULADA
