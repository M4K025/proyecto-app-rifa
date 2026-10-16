"""FRONTEND CLI: menú completo. Solo habla con la API, nunca con BACK ni ORM directo."""
from ..api.contratos import ApartarRequest, ComprarRequest, CrearRifaRequest
from ..back.dominio.enums import MetodoPago


def _input(msg, default=""):
    v = input(f"{msg} [{default}]: ").strip()
    return v or default


def main(api):
    print("== RIFA APP (FRONTEND -> API -> BACK -> ORM) ==")
    while True:
        print("\n1.Crear rifa 2.Ver rifas 3.Tablero 4.Registrarse 5.Apartar 6.Comprar 7.Sorteo 8.Reporte 0.Salir")
        op = _input("Opción", "0")
        try:
            if op == "1":
                t = _input("Título", "Rifa 2.000.000"); p = float(_input("Precio", "50000")); c = int(_input("Cantidad", "10"))
                rifa, meta = api.post_rifas(CrearRifaRequest(t, p, c))
                print(f"Rifa {rifa.id} creada, {c} boletos de ${p:,.0f}. Meta ${meta.monto_meta:,.0f}")
            elif op == "2":
                for r in api.get_rifas():
                    print(f"#{r.id} {r.titulo} ${r.monto_recaudado:,.0f}/${r.objetivo:,.0f} {r.estado.value}")
            elif op == "3":
                rid = int(_input("Rifa id", "1"))
                for b in api.get_tablero(rid):
                    print(f"boleto id={b.id} nro={b.numero} ${b.precio:,.0f} {b.estado.value}")
            elif op == "4":
                u = api.post_usuarios(_input("Nombre", "Ana"), _input("Correo", "ana@mail.com"))
                print(f"Usuario {u.id} {u.nombre}")
            elif op == "5":
                b = api.post_apartar(ApartarRequest(int(_input("Boleto id", "1")), int(_input("Usuario id", "1"))))
                print(f"Apartado #{b.numero} -> {b.estado.value}")
            elif op == "6":
                uid = int(_input("Usuario id", "1")); bids = [int(x) for x in _input("Boletos ids (coma)", "1").split(",")]
                compra, pago, comp = api.post_compras(ComprarRequest(uid, bids, MetodoPago.EFECTIVO))
                print(f"Compra {compra.id} total=${compra.total:,.0f} {compra.estado.value} | {comp.enviar_por_correo('correo')}")
            elif op == "7":
                s = api.post_sorteo(int(_input("Rifa id", "1")))
                print(f"Ganador boleto id={s.ganador_boleto_id}")
            elif op == "8":
                rid = int(_input("Rifa id", "1"))
                rifas = [r for r in api.get_rifas() if r.id == rid] or api.rifa.rifas.listar()
                r = next((x for x in rifas if x.id == rid), None)
                rep = api.get_reporte(rid, recaudado=r.monto_recaudado if r else 0, objetivo=r.objetivo if r else 2000000)
                print(rep.exportar())
            elif op == "0":
                break
        except Exception as e:
            print(f"Error: {e}")
