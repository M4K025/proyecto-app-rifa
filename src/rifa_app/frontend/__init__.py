"""Capa FRONTEND: pantallas de la app móvil y a qué endpoint pegan + CLI completa."""
from .app_cli import main as cli_main

PANTALLAS = {
    "Registro": {"botones": ["Registrarse", "Crear"], "api": ["POST /api/usuarios"]},
    "Crear rifa": {"campos": ["Foto", "Datos objeto", "Organizador", "Info sorteo"], "api": ["POST /api/rifas"]},
    "Ficha premio": {"muestra": ["foto", "precio", "fecha/hora", "disponibles/apartados/pagados"], "api": ["GET /api/rifas/{id}/boletos"]},
    "Tablero": {"grilla": "00-99 por EstadoBoleto", "api": ["POST /api/boletos/{id}/apartar", "POST /api/compras"]},
    "Pagar": {"campos": ["nombre", "correo", "teléfono", "documento", "método"], "api": ["POST /api/compras", "POST /api/pagos/{id}/aprobar"]},
    "Mis rifas": {"listas": ["participadas", "creadas"], "api": ["GET /api/rifas", "GET /api/reportes"]},
}

__all__ = ["PANTALLAS", "cli_main"]
