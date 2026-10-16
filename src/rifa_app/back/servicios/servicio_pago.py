class ServicioPago:

    def __init__(self, repo_pagos):
        self.pagos = repo_pagos

    def aprobar(self, pago_id: int):
        p = self.pagos.obtener(pago_id)
        if not p:
            raise ValueError('pago no existe')
        p.aprobar()
        return self.pagos.guardar(p)

    def rechazar(self, pago_id: int):
        p = self.pagos.obtener(pago_id)
        if not p:
            raise ValueError('pago no existe')
        p.rechazar()
        return self.pagos.guardar(p)

    def pendientes(self):
        from ..dominio import EstadoPago
        return self.pagos.buscar_por(estado=EstadoPago.PENDIENTE)
