from dataclasses import dataclass


@dataclass
class MetaRecaudacion:
    """Tu cuadro MetaRecaudación separado de Rifa."""
    id: int
    rifa_id: int
    monto_meta: float = 900_000.0
    monto_actual: float = 0.0

    def actualizar_monto(self, valor: float) -> None:
        self.monto_actual += valor

    def porcentaje(self) -> float:
        if self.monto_meta == 0:
            return 0.0
        return round(self.monto_actual / self.monto_meta * 100, 2)

    def cumple_meta(self) -> bool:
        return self.monto_actual >= self.monto_meta
