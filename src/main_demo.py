import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rifa_app.back.dominio.enums import MetodoPago, TipoReporte
from rifa_app.back.dominio.usuario import Usuario
from rifa_app.orm.base import RepositorioMemoria
from rifa_app.back.servicios.servicio_rifa import ServicioRifa
from rifa_app.back.servicios.servicio_boleto import ServicioBoleto
from rifa_app.back.servicios.servicio_compra import ServicioCompra
from rifa_app.back.servicios.servicio_reporte import ServicioReporte
from rifa_app.api.contratos import ComprarRequest
from rifa_app.api import post_compras

def main() -> None:
    r_usuarios, r_rifas, r_boletos = (RepositorioMemoria(), RepositorioMemoria(), RepositorioMemoria())
    r_compras, r_pagos, r_metas = (RepositorioMemoria(), RepositorioMemoria(), RepositorioMemoria())
    r_reportes, r_comprob = (RepositorioMemoria(), RepositorioMemoria())
    s_rifa = ServicioRifa(r_rifas, r_metas)
    s_boleto = ServicioBoleto(r_boletos)
    s_compra = ServicioCompra(r_compras, r_pagos, r_boletos, r_rifas, r_metas, r_comprob)
    s_reporte = ServicioReporte(r_reportes, r_boletos)
    rifa, meta = s_rifa.crear_rifa('Rifa 2.000.000', precio_boleto=50000, cantidad_boletos=40, descripcion='Premio en efectivo', objetivo=2000000.0)
    s_boleto.generar_boletos(rifa.id, 40, 50000)
    print(f"Rifa {rifa.id} '{rifa.titulo}' objetivo={rifa.objetivo} disponibles={len(s_boleto.disponibles(rifa.id))}")
    u = r_usuarios.guardar(Usuario(id=0, nombre='Ana', correo='ana@mail.com', telefono='300123'))
    u.registrar()
    boleto5 = [b for b in r_boletos.listar() if b.numero == 5][0]
    req = ComprarRequest(usuario_id=u.id, boleto_ids=[boleto5.id], metodo=MetodoPago.EFECTIVO)
    compra, pago, comp = post_compras(req, s_compra)
    print(f'Compra {compra.id} total={compra.total} estado={compra.estado.value} pago={pago.estado.value}')
    print(comp.enviar_por_correo(u.correo))
    rep = s_reporte.generar(rifa.id, TipoReporte.RECAUDACION, recaudado=rifa.monto_recaudado, objetivo=rifa.objetivo)
    print(rep.exportar())
    print(f'Meta: {meta.monto_actual}/{meta.monto_meta} ({meta.porcentaje()}%) cumple={meta.cumple_meta()} rifa_meta={rifa.verificar_meta()}')
if __name__ == '__main__':
    main()
