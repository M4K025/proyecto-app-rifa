from datetime import datetime
from .database import Database
from ..back.dominio import Boleto, Compra, Comprobante, MetaRecaudacion, Pago, Reporte, Rifa, Sorteo, Usuario
from ..back.dominio.enums import EstadoBoleto, EstadoCompra, EstadoPago, EstadoRifa, MetodoPago, RolUsuario, TipoReporte

def _v(x):
    return x.value if hasattr(x, 'value') else x

def _dt(x):
    if not x:
        return None
    return x.isoformat() if hasattr(x, 'isoformat') else str(x)

def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None

class RepoUsuarios:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, u: Usuario) -> Usuario:
        if u.id:
            self.db.execute('UPDATE usuarios SET nombre=?,correo=?,telefono=?,documento=?,rol=? WHERE id=?', (u.nombre, u.correo, u.telefono, u.documento, _v(u.rol), u.id))
        else:
            cur = self.db.execute('INSERT INTO usuarios(nombre,correo,telefono,documento,rol) VALUES(?,?,?,?,?)', (u.nombre, u.correo, u.telefono, u.documento, _v(u.rol)))
            u.id = cur.lastrowid
        return u

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM usuarios WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM usuarios')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        v = _v(v)
        return [self._map(r) for r in self.db.query(f'SELECT * FROM usuarios WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM usuarios WHERE id=?', (i,))

    def _map(self, r):
        return Usuario(r['id'], r['nombre'], r['correo'], r['telefono'] or '', r['documento'] or '', RolUsuario(r['rol']))

class RepoRifas:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, x: Rifa) -> Rifa:
        vals = (x.titulo, x.descripcion, x.objetivo, x.monto_recaudado, _dt(x.fecha_inicio), _dt(x.fecha_fin), _v(x.estado), x.premio_nombre, int(x.premio_usado))
        if x.id:
            self.db.execute('UPDATE rifas SET titulo=?,descripcion=?,objetivo=?,monto_recaudado=?,fecha_inicio=?,fecha_fin=?,estado=?,premio_nombre=?,premio_usado=? WHERE id=?', (*vals, x.id))
        else:
            cur = self.db.execute('INSERT INTO rifas(titulo,descripcion,objetivo,monto_recaudado,fecha_inicio,fecha_fin,estado,premio_nombre,premio_usado) VALUES(?,?,?,?,?,?,?,?,?)', vals)
            x.id = cur.lastrowid
        return x

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM rifas WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM rifas')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        v = _v(v)
        return [self._map(r) for r in self.db.query(f'SELECT * FROM rifas WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM rifas WHERE id=?', (i,))

    def _map(self, r):
        from datetime import date

        def _d(s):
            if not s:
                return None
            try:
                return date.fromisoformat(s)
            except ValueError:
                return None
        return Rifa(r['id'], r['titulo'], r['descripcion'] or '', r['objetivo'], r['monto_recaudado'], _d(r['fecha_inicio']), _d(r['fecha_fin']), EstadoRifa(r['estado']), r['premio_nombre'] or '', bool(r['premio_usado']))

class RepoBoletos:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, b: Boleto) -> Boleto:
        vals = (b.numero, b.precio, b.rifa_id, _v(b.estado), _dt(b.fecha_apartado), b.comprador_id, b.vendedor_id)
        if b.id:
            self.db.execute('UPDATE boletos SET numero=?,precio=?,rifa_id=?,estado=?,fecha_apartado=?,comprador_id=?,vendedor_id=? WHERE id=?', (*vals, b.id))
        else:
            cur = self.db.execute('INSERT INTO boletos(numero,precio,rifa_id,estado,fecha_apartado,comprador_id,vendedor_id) VALUES(?,?,?,?,?,?,?)', vals)
            b.id = cur.lastrowid
        return b

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM boletos WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM boletos')]

    def buscar_por(self, **f):
        cond = ' AND '.join((f'{k}=?' for k in f))
        vals = tuple((_v(v) for v in f.values()))
        return [self._map(r) for r in self.db.query(f'SELECT * FROM boletos WHERE {cond}', vals)]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM boletos WHERE id=?', (i,))

    def _map(self, r):
        return Boleto(r['id'], r['numero'], r['precio'], r['rifa_id'], EstadoBoleto(r['estado']), _parse_dt(r['fecha_apartado']), r['comprador_id'], r['vendedor_id'])

class RepoCompras:

    def __init__(self, db: Database, repo_boletos: RepoBoletos):
        self.db = db
        self.rb = repo_boletos

    def guardar(self, c: Compra) -> Compra:
        if c.id:
            self.db.execute('UPDATE compras SET usuario_id=?,metodo_pago=?,estado=?,fecha=? WHERE id=?', (c.usuario_id, _v(c.metodo_pago), _v(c.estado), _dt(c.fecha), c.id))
        else:
            cur = self.db.execute('INSERT INTO compras(usuario_id,metodo_pago,estado,fecha) VALUES(?,?,?,?)', (c.usuario_id, _v(c.metodo_pago), _v(c.estado), _dt(c.fecha)))
            c.id = cur.lastrowid
        for b in c.boletos:
            if b.id and (not b.id in [0, None]):
                self.rb.guardar(b)
                self.db.execute('INSERT OR IGNORE INTO compra_boletos(compra_id,boleto_id) VALUES(?,?)', (c.id, b.id))
        return c

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM compras WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM compras')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        v = _v(v)
        return [self._map(r) for r in self.db.query(f'SELECT * FROM compras WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM compra_boletos WHERE compra_id=?', (i,))
        self.db.execute('DELETE FROM compras WHERE id=?', (i,))

    def _map(self, r):
        ids = [x['boleto_id'] for x in self.db.query('SELECT boleto_id FROM compra_boletos WHERE compra_id=?', (r['id'],))]
        bols = [self.rb.obtener(i) for i in ids]
        bols = [b for b in bols if b]
        return Compra(r['id'], r['usuario_id'], bols, MetodoPago(r['metodo_pago']), EstadoCompra(r['estado']), _parse_dt(r['fecha']) or datetime.now())

class RepoPagos:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, p: Pago) -> Pago:
        if p.id:
            self.db.execute('UPDATE pagos SET compra_id=?,monto=?,referencia=?,estado=?,fecha=? WHERE id=?', (p.compra_id, p.monto, p.referencia, _v(p.estado), _dt(p.fecha), p.id))
        else:
            cur = self.db.execute('INSERT INTO pagos(compra_id,monto,referencia,estado,fecha) VALUES(?,?,?,?,?)', (p.compra_id, p.monto, p.referencia, _v(p.estado), _dt(p.fecha)))
            p.id = cur.lastrowid
        return p

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM pagos WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM pagos')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        v = _v(v)
        return [self._map(r) for r in self.db.query(f'SELECT * FROM pagos WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM pagos WHERE id=?', (i,))

    def _map(self, r):
        return Pago(r['id'], r['compra_id'], r['monto'], r['referencia'] or '', EstadoPago(r['estado']), _parse_dt(r['fecha']) or datetime.now())

class RepoSorteos:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, s: Sorteo) -> Sorteo:
        if s.id:
            self.db.execute('UPDATE sorteos SET rifa_id=?,fecha_sorteo=?,ganador_boleto_id=?,estado=? WHERE id=?', (s.rifa_id, _dt(s.fecha_sorteo), s.ganador_boleto_id, _v(s.estado), s.id))
        else:
            cur = self.db.execute('INSERT INTO sorteos(rifa_id,fecha_sorteo,ganador_boleto_id,estado) VALUES(?,?,?,?)', (s.rifa_id, _dt(s.fecha_sorteo), s.ganador_boleto_id, _v(s.estado)))
            s.id = cur.lastrowid
        return s

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM sorteos WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM sorteos')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        v = _v(v)
        return [self._map(r) for r in self.db.query(f'SELECT * FROM sorteos WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM sorteos WHERE id=?', (i,))

    def _map(self, r):
        return Sorteo(r['id'], r['rifa_id'], _parse_dt(r['fecha_sorteo']) or datetime.now(), r['ganador_boleto_id'], EstadoRifa(r['estado']))

class RepoMetas:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, m: MetaRecaudacion) -> MetaRecaudacion:
        if m.id:
            self.db.execute('UPDATE metas SET rifa_id=?,monto_meta=?,monto_actual=? WHERE id=?', (m.rifa_id, m.monto_meta, m.monto_actual, m.id))
        else:
            cur = self.db.execute('INSERT INTO metas(rifa_id,monto_meta,monto_actual) VALUES(?,?,?)', (m.rifa_id, m.monto_meta, m.monto_actual))
            m.id = cur.lastrowid
        return m

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM metas WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM metas')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        return [self._map(r) for r in self.db.query(f'SELECT * FROM metas WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM metas WHERE id=?', (i,))

    def _map(self, r):
        return MetaRecaudacion(r['id'], r['rifa_id'], r['monto_meta'], r['monto_actual'])

class RepoReportes:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, x: Reporte) -> Reporte:
        if x.id:
            self.db.execute('UPDATE reportes SET rifa_id=?,tipo=?,fecha_generacion=?,contenido=? WHERE id=?', (x.rifa_id, _v(x.tipo), _dt(x.fecha_generacion), x.contenido, x.id))
        else:
            cur = self.db.execute('INSERT INTO reportes(rifa_id,tipo,fecha_generacion,contenido) VALUES(?,?,?,?)', (x.rifa_id, _v(x.tipo), _dt(x.fecha_generacion), x.contenido))
            x.id = cur.lastrowid
        return x

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM reportes WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM reportes')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        v = _v(v)
        return [self._map(r) for r in self.db.query(f'SELECT * FROM reportes WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM reportes WHERE id=?', (i,))

    def _map(self, r):
        return Reporte(r['id'], r['rifa_id'], TipoReporte(r['tipo']), _parse_dt(r['fecha_generacion']) or datetime.now(), r['contenido'] or '')

class RepoComprobantes:

    def __init__(self, db: Database):
        self.db = db

    def guardar(self, c: Comprobante) -> Comprobante:
        if c.id:
            self.db.execute('UPDATE comprobantes SET compra_id=?,codigo_qr=?,fecha_emision=? WHERE id=?', (c.compra_id, c.codigo_qr, _dt(c.fecha_emision), c.id))
        else:
            cur = self.db.execute('INSERT INTO comprobantes(compra_id,codigo_qr,fecha_emision) VALUES(?,?,?)', (c.compra_id, c.codigo_qr, _dt(c.fecha_emision)))
            c.id = cur.lastrowid
        return c

    def obtener(self, i: int):
        r = self.db.query('SELECT * FROM comprobantes WHERE id=?', (i,))
        return self._map(r[0]) if r else None

    def listar(self):
        return [self._map(r) for r in self.db.query('SELECT * FROM comprobantes')]

    def buscar_por(self, **f):
        k, v = next(iter(f.items()))
        return [self._map(r) for r in self.db.query(f'SELECT * FROM comprobantes WHERE {k}=?', (v,))]

    def eliminar(self, i: int):
        self.db.execute('DELETE FROM comprobantes WHERE id=?', (i,))

    def _map(self, r):
        return Comprobante(r['id'], r['compra_id'], r['codigo_qr'] or '', _parse_dt(r['fecha_emision']) or datetime.now())
