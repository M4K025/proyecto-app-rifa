from ..dominio import Boleto, EstadoBoleto, Reporte, TipoReporte

class ServicioReporte:

    def __init__(self, repo_reportes, repo_boletos):
        self.reportes = repo_reportes
        self.boletos = repo_boletos

    def generar(self, rifa_id: int, tipo: TipoReporte=TipoReporte.RECAUDACION, recaudado: float=0, objetivo: float=2000000) -> Reporte:
        bol = self.boletos.buscar_por(rifa_id=rifa_id)
        disp = sum((1 for b in bol if b.estado == EstadoBoleto.DISPONIBLE))
        vend = sum((1 for b in bol if b.estado in (EstadoBoleto.VENDIDO, EstadoBoleto.PAGADO)))
        rep = Reporte(id=0, rifa_id=rifa_id, tipo=tipo)
        rep.generar(f'recaudado={recaudado} objetivo={objetivo} boletos={len(bol)} vendidos={vend} disponibles={disp}')
        return self.reportes.guardar(rep)
