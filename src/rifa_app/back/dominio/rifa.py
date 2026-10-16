from dataclasses import dataclass, field
from datetime import date
from .enums import EstadoRifa


@dataclass
class Rifa:
    id: int
    titulo: str
    descripcion: str = ""
    objetivo: float = 900_000.0
    monto_recaudado: float = 0.0
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    estado: EstadoRifa = EstadoRifa.ACTIVA
    # Datos del premio (de tus mockups: objeto, tamaño, color, usado, contacto)
    premio_nombre: str = ""
    premio_usado: bool = False

    def crear(self) -> None:
        if self.objetivo <= 0:
            raise ValueError("objetivo debe ser > 0")
        self.estado = EstadoRifa.ACTIVA

    def actualizar(self, **cambios) -> None:
        for k, v in cambios.items():
            setattr(self, k, v)

    def verificar_meta(self) -> bool:
        return self.monto_recaudado >= self.objetivo

    def abonar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("abono debe ser > 0")
        self.monto_recaudado += valor
