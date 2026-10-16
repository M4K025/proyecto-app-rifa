from ..dominio import Boleto, EstadoBoleto

class ServicioBoleto:

    def __init__(self, repo):
        self.repo = repo

    def generar_boletos(self, rifa_id: int, cantidad: int, precio: float) -> list[Boleto]:
        out = []
        for n in range(cantidad):
            b = Boleto(id=0, numero=n, precio=precio, rifa_id=rifa_id)
            out.append(self.repo.guardar(b))
        return out

    def disponibles(self, rifa_id: int) -> list[Boleto]:
        return [b for b in self.repo.buscar_por(rifa_id=rifa_id) if b.estado == EstadoBoleto.DISPONIBLE]

    def apartar(self, boleto_id: int, comprador_id: int) -> Boleto:
        b = self.repo.obtener(boleto_id)
        if not b:
            raise ValueError('boleto no existe')
        b.reservar(comprador_id)
        return self.repo.guardar(b)

    def liberar(self, boleto_id: int) -> Boleto:
        b = self.repo.obtener(boleto_id)
        if not b:
            raise ValueError('boleto no existe')
        b.liberar()
        return self.repo.guardar(b)
