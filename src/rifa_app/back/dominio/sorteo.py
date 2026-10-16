import random
from dataclasses import dataclass
from datetime import datetime
from .enums import EstadoRifa


@dataclass
class Sorteo:
    id: int
    rifa_id: int
    fecha_sorteo: datetime
    ganador_boleto_id: int | None = None
    estado: EstadoRifa = EstadoRifa.ACTIVA

    def realizar_sorteo(self, boletos_vendidos_ids: list[int], seed: int | None = None) -> int:
        if not boletos_vendidos_ids:
            raise ValueError("no hay boletos vendidos para sortear")
        rng = random.Random(seed)
        self.ganador_boleto_id = rng.choice(boletos_vendidos_ids)
        return self.ganador_boleto_id
