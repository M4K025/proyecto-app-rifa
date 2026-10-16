from dataclasses import dataclass
from .enums import RolUsuario

@dataclass
class Usuario:
    id: int
    nombre: str
    correo: str
    telefono: str = ''
    documento: str = ''
    rol: RolUsuario = RolUsuario.CLIENTE

    def registrar(self) -> None:
        if '@' not in self.correo:
            raise ValueError('correo inválido')

    def iniciar_sesion(self) -> bool:
        return bool(self.correo)

    def actualizar(self, **cambios) -> None:
        for k, v in cambios.items():
            setattr(self, k, v)
