from .contratos import ApartarRequest, ComprarRequest, CrearRifaRequest, ENDPOINTS
from .controladores import Api
__all__ = ['CrearRifaRequest', 'ApartarRequest', 'ComprarRequest', 'ENDPOINTS', 'Api']

def post_compras(comprar: ComprarRequest, servicio):
    return servicio.comprar(comprar.usuario_id, comprar.boleto_ids, comprar.metodo)
