import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rifa_app.api.controladores import Api
from rifa_app.back.servicios import ServicioUsuario, ServicioRifa, ServicioBoleto, ServicioCompra, ServicioPago, ServicioSorteo, ServicioReporte
from rifa_app.frontend.app_cli import main as cli_main
from rifa_app.orm import Database, RepoUsuarios, RepoRifas, RepoBoletos, RepoCompras, RepoPagos, RepoSorteos, RepoMetas, RepoReportes, RepoComprobantes

def crear_api(ruta_db: str='rifa.db') -> tuple[Api, Database]:
    db = Database(ruta_db)
    ru, rr, rb = (RepoUsuarios(db), RepoRifas(db), RepoBoletos(db))
    rm = RepoMetas(db)
    rc = RepoCompras(db, rb)
    rp, rs = (RepoPagos(db), RepoSorteos(db))
    rrep, rcomp = (RepoReportes(db), RepoComprobantes(db))
    api = Api(ServicioUsuario(ru), ServicioRifa(rr, rm), ServicioBoleto(rb), ServicioCompra(rc, rp, rb, rr, rm, rcomp), ServicioPago(rp), ServicioSorteo(rs, rb), ServicioReporte(rrep, rb))
    return (api, db)
if __name__ == '__main__':
    api, _ = crear_api()
    cli_main(api)
