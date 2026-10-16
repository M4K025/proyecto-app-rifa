"""Prueba final: flujo completo contra ORM en memoria temporal (SQLite :memory:)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import crear_api
from rifa_app.api.contratos import ComprarRequest, CrearRifaRequest
from rifa_app.back.dominio.enums import MetodoPago


def test_producto_final():
    api, _ = crear_api(":memory:")
    u = api.post_usuarios("Ana", "ana@mail.com", telefono="300")
    rifa, meta = api.post_rifas(CrearRifaRequest("Rifa 2.000.000", 50_000, 10))
    assert len(api.get_tablero(rifa.id)) == 10
    b5 = [b for b in api.get_tablero(rifa.id) if b.numero == 5][0]
    compra, pago, comp = api.post_compras(ComprarRequest(u.id, [b5.id], MetodoPago.EFECTIVO))
    assert compra.total == 50_000 and pago.estado.value == "APROBADO"
    rep = api.get_reporte(rifa.id, recaudado=api.rifa.rifas.obtener(rifa.id).monto_recaudado)
    assert "vendidos=1" in rep.contenido
    sorteo = api.post_sorteo(rifa.id)
    assert sorteo.ganador_boleto_id == b5.id
    print("OK producto final: rifa+compra+pago+reporte+sorteo con ORM SQLite")


if __name__ == "__main__":
    test_producto_final()
