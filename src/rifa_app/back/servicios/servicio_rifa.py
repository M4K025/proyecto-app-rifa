from ..dominio import EstadoRifa, Rifa, MetaRecaudacion


class ServicioRifa:
    def __init__(self, repo_rifas, repo_metas):
        self.rifas = repo_rifas
        self.metas = repo_metas

    def crear_rifa(self, titulo: str, precio_boleto: float, cantidad_boletos: int, **extra) -> tuple[Rifa, MetaRecaudacion]:
        rifa = Rifa(id=0, titulo=titulo, **extra)
        rifa.crear()
        self.rifas.guardar(rifa)
        meta = MetaRecaudacion(id=0, rifa_id=rifa.id, monto_meta=rifa.objetivo)
        self.metas.guardar(meta)
        self._precio_default = precio_boleto
        self._cantidad_default = cantidad_boletos
        return rifa, meta

    def listar_activas(self):
        return self.rifas.buscar_por(estado=EstadoRifa.ACTIVA)

    def finalizar(self, rifa_id: int):
        r = self.rifas.obtener(rifa_id)
        if not r:
            raise ValueError("rifa no existe")
        r.estado = EstadoRifa.FINALIZADA
        return self.rifas.guardar(r)
