"""Implementa el diagrama de actividad Comprar Boleta."""
from ..dominio import Boleto, Compra, Comprobante, MetodoPago, Pago, Rifa, MetaRecaudacion


class ServicioCompra:
    def __init__(self, repo_compras, repo_pagos, repo_boletos, repo_rifas, repo_metas, repo_comprobantes):
        self.compras = repo_compras
        self.pagos = repo_pagos
        self.boletos = repo_boletos
        self.rifas = repo_rifas
        self.metas = repo_metas
        self.comprobantes = repo_comprobantes

    def comprar(self, usuario_id: int, boleto_ids: list[int], metodo: MetodoPago = MetodoPago.EFECTIVO) -> tuple[Compra, Pago, Comprobante]:
        boletos = [self.boletos.obtener(i) for i in boleto_ids]
        if any(b is None for b in boletos):
            raise ValueError("boleto inexistente")
        for b in boletos:
            if b.estado.value not in ("DISPONIBLE", "APARTADO"):
                raise ValueError(f"boleto {b.numero} no disponible")
            if b.estado.value == "DISPONIBLE":
                b.reservar(usuario_id)
                self.boletos.guardar(b)

        compra = Compra(id=0, usuario_id=usuario_id, boletos=[b for b in boletos if b is not None], metodo_pago=metodo)
        self.compras.guardar(compra)

        pago = Pago(id=0, compra_id=compra.id, monto=compra.calcular_total(), referencia=f"REF-{compra.id}")
        pago.aprobar()
        self.pagos.guardar(pago)

        compra.confirmar()
        self.compras.guardar(compra)
        for b in boletos:
            self.boletos.guardar(b)

        rifa = self.rifas.obtener(boletos[0].rifa_id)
        if rifa:
            rifa.abonar(pago.monto)
            self.rifas.guardar(rifa)
            for m in self.metas.buscar_por(rifa_id=rifa.id):
                m.actualizar_monto(pago.monto)
                self.metas.guardar(m)

        comp = Comprobante(id=0, compra_id=compra.id, codigo_qr=f"QR-{compra.id}")
        self.comprobantes.guardar(comp)
        return compra, pago, comp

    def cancelar(self, compra_id: int):
        c = self.compras.obtener(compra_id)
        if not c:
            raise ValueError("compra no existe")
        c.anular()
        for b in c.boletos:
            self.boletos.guardar(b)
        return self.compras.guardar(c)
