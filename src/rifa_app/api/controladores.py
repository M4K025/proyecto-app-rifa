from .contratos import ApartarRequest, ComprarRequest, CrearRifaRequest, ENDPOINTS

class Api:

    def __init__(self, s_usuario, s_rifa, s_boleto, s_compra, s_pago, s_sorteo, s_reporte):
        self.u, self.rifa, self.bol = (s_usuario, s_rifa, s_boleto)
        self.compra, self.pago = (s_compra, s_pago)
        self.sorteo, self.rep = (s_sorteo, s_reporte)

    def post_usuarios(self, nombre, correo, **extra):
        return self.u.registrar(nombre, correo, **extra)

    def post_rifas(self, req: CrearRifaRequest):
        rifa, meta = self.rifa.crear_rifa(req.titulo, req.precio_boleto, req.cantidad_boletos, objetivo=req.objetivo)
        self.bol.generar_boletos(rifa.id, req.cantidad_boletos, req.precio_boleto)
        return (rifa, meta)

    def get_rifas(self):
        return self.rifa.listar_activas()

    def get_tablero(self, rifa_id: int):
        return self.bol.repo.buscar_por(rifa_id=rifa_id)

    def post_apartar(self, req: ApartarRequest):
        return self.bol.apartar(req.boleto_id, req.comprador_id)

    def post_compras(self, req: ComprarRequest):
        return self.compra.comprar(req.usuario_id, req.boleto_ids, req.metodo)

    def post_pago_aprobar(self, pago_id: int):
        return self.pago.aprobar(pago_id)

    def post_sorteo(self, rifa_id: int):
        return self.sorteo.realizar(rifa_id)

    def get_reporte(self, rifa_id: int, tipo='RECAUDACION', recaudado=0, objetivo=2000000):
        from ..back.dominio.enums import TipoReporte
        return self.rep.generar(rifa_id, TipoReporte(tipo), recaudado, objetivo)
