"""Capa API: contratos REST que el FRONTEND consume. Sin lógica, solo delega al BACK."""
from .contratos import ApartarRequest, ComprarRequest, CrearRifaRequest, ENDPOINTS
from .controladores import Api

__all__ = ["CrearRifaRequest", "ApartarRequest", "ComprarRequest", "ENDPOINTS", "Api"]


def post_compras(comprar: ComprarRequest, servicio):
    """Compat: POST /api/compras directo al servicio (demo rápida)."""
    return servicio.comprar(comprar.usuario_id, comprar.boleto_ids, comprar.metodo)
