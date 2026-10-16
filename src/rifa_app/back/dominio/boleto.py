from dataclasses import dataclass
from datetime import datetime
from .enums import EstadoBoleto

@dataclass
class Boleto:
    id: int
    numero: int
    precio: float
    rifa_id: int
    estado: EstadoBoleto = EstadoBoleto.DISPONIBLE
    fecha_apartado: datetime | None = None
    comprador_id: int | None = None
    vendedor_id: int | None = None

    def reservar(self, comprador_id: int) -> None:
        if self.estado != EstadoBoleto.DISPONIBLE:
            raise ValueError(f'boleto {self.numero} no disponible ({self.estado})')
        self.estado = EstadoBoleto.APARTADO
        self.comprador_id = comprador_id
        self.fecha_apartado = datetime.now()

    def marcar_vendido(self) -> None:
        if self.estado not in (EstadoBoleto.APARTADO, EstadoBoleto.PAGADO):
            raise ValueError('solo un boleto apartado/pagado se puede vender')
        self.estado = EstadoBoleto.VENDIDO

    def liberar(self) -> None:
        self.estado = EstadoBoleto.DISPONIBLE
        self.comprador_id = None
        self.fecha_apartado = None
