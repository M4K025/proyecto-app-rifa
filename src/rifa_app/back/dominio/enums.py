"""Enums del dominio. Evitan strings mágicos como 'apartado'/'Apartado'."""
from enum import Enum


class RolUsuario(str, Enum):
    ADMIN = "ADMIN"
    ORGANIZADOR = "ORGANIZADOR"
    VENDEDOR = "VENDEDOR"
    CLIENTE = "CLIENTE"


class EstadoRifa(str, Enum):
    ACTIVA = "ACTIVA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"


class EstadoBoleto(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    APARTADO = "APARTADO"
    PAGADO = "PAGADO"
    VENDIDO = "VENDIDO"
    RECHAZADO = "RECHAZADO"


class EstadoCompra(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    ANULADA = "ANULADA"


class MetodoPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA = "TRANSFERENCIA"
    TARJETA = "TARJETA"
    PSE = "PSE"


class EstadoPago(str, Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class TipoReporte(str, Enum):
    CUENTAS = "CUENTAS"
    RECAUDACION = "RECAUDACION"
    BOLETOS = "BOLETOS"
