"""Capa ORM: mapeo Objeto-Relacional con sqlite3 (stdlib, sin dependencias).

Tablas = una por entidad del BACK. Los repositorios convierten fila <-> objeto.
Así se cumple POO de clase: el BACK no escribe SQL, el ORM sí.
"""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, correo TEXT UNIQUE, telefono TEXT, documento TEXT, rol TEXT);
CREATE TABLE IF NOT EXISTS rifas(id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, descripcion TEXT, objetivo REAL, monto_recaudado REAL, fecha_inicio TEXT, fecha_fin TEXT, estado TEXT, premio_nombre TEXT, premio_usado INTEGER);
CREATE TABLE IF NOT EXISTS boletos(id INTEGER PRIMARY KEY AUTOINCREMENT, numero INTEGER, precio REAL, rifa_id INTEGER, estado TEXT, fecha_apartado TEXT, comprador_id INTEGER, vendedor_id INTEGER);
CREATE TABLE IF NOT EXISTS compras(id INTEGER PRIMARY KEY AUTOINCREMENT, usuario_id INTEGER, metodo_pago TEXT, estado TEXT, fecha TEXT);
CREATE TABLE IF NOT EXISTS compra_boletos(compra_id INTEGER, boleto_id INTEGER, PRIMARY KEY(compra_id, boleto_id));
CREATE TABLE IF NOT EXISTS pagos(id INTEGER PRIMARY KEY AUTOINCREMENT, compra_id INTEGER, monto REAL, referencia TEXT, estado TEXT, fecha TEXT);
CREATE TABLE IF NOT EXISTS sorteos(id INTEGER PRIMARY KEY AUTOINCREMENT, rifa_id INTEGER, fecha_sorteo TEXT, ganador_boleto_id INTEGER, estado TEXT);
CREATE TABLE IF NOT EXISTS metas(id INTEGER PRIMARY KEY AUTOINCREMENT, rifa_id INTEGER, monto_meta REAL, monto_actual REAL);
CREATE TABLE IF NOT EXISTS reportes(id INTEGER PRIMARY KEY AUTOINCREMENT, rifa_id INTEGER, tipo TEXT, fecha_generacion TEXT, contenido TEXT);
CREATE TABLE IF NOT EXISTS comprobantes(id INTEGER PRIMARY KEY AUTOINCREMENT, compra_id INTEGER, codigo_qr TEXT, fecha_emision TEXT);
"""


class Database:
    def __init__(self, ruta: str = "rifa.db"):
        self.ruta = ruta
        self.conn = sqlite3.connect(ruta)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def execute(self, sql: str, params: tuple = ()):
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql: str, params: tuple = ()):
        return self.conn.execute(sql, params).fetchall()

    def close(self):
        self.conn.close()
