"""DTOs + catálogo de endpoints (para revisión con el equipo frontend)."""
from dataclasses import dataclass
from ..back.dominio.enums import MetodoPago

ENDPOINTS = [
    ("POST", "/api/rifas", "Crear rifa (organizador)"),
    ("GET", "/api/rifas", "Listar rifas activas"),
    ("GET", "/api/rifas/{id}/boletos?estado=DISPONIBLE", "Tablero de números"),
    ("POST", "/api/boletos/{id}/apartar", "Apartar boleto"),
    ("POST", "/api/compras", "Comprar (apartar+ pagar + comprobante)"),
    ("POST", "/api/pagos/{id}/aprobar", "Aprobar pago (organizador)"),
    ("POST", "/api/sorteos", "Realizar sorteo"),
    ("GET", "/api/reportes?rifa={id}&tipo=RECAUDACION", "Reporte recaudado vs $900.000"),
]


@dataclass
class CrearRifaRequest:
    titulo: str
    precio_boleto: float
    cantidad_boletos: int
    objetivo: float = 900_000.0


@dataclass
class ApartarRequest:
    boleto_id: int
    comprador_id: int


@dataclass
class ComprarRequest:
    usuario_id: int
    boleto_ids: list[int]
    metodo: MetodoPago = MetodoPago.EFECTIVO
