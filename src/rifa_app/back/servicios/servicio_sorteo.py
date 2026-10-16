from datetime import datetime
from ..dominio import EstadoBoleto, Sorteo


class ServicioSorteo:
    def __init__(self, repo_sorteos, repo_boletos):
        self.sorteos = repo_sorteos
        self.boletos = repo_boletos

    def realizar(self, rifa_id: int, seed: int | None = None) -> Sorteo:
        vendidos = [b for b in self.boletos.buscar_por(rifa_id=rifa_id)
                    if b.estado in (EstadoBoleto.VENDIDO, EstadoBoleto.PAGADO)]
        if not vendidos:
            raise ValueError("no hay boletos vendidos para sortear")
        s = Sorteo(id=0, rifa_id=rifa_id, fecha_sorteo=datetime.now())
        s.realizar_sorteo([b.id for b in vendidos], seed=seed)
        return self.sorteos.guardar(s)
