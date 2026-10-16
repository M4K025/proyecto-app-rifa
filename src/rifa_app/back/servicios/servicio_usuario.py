from ..dominio import Usuario


class ServicioUsuario:
    def __init__(self, repo):
        self.repo = repo

    def registrar(self, nombre: str, correo: str, telefono: str = "", documento: str = "", rol="CLIENTE") -> Usuario:
        from ..dominio.enums import RolUsuario
        u = Usuario(id=0, nombre=nombre, correo=correo, telefono=telefono, documento=documento,
                    rol=rol if isinstance(rol, RolUsuario) else RolUsuario(rol))
        u.registrar()
        if self.repo.buscar_por(correo=correo):
            raise ValueError("correo ya registrado")
        return self.repo.guardar(u)

    def login(self, correo: str):
        r = self.repo.buscar_por(correo=correo)
        if not r:
            raise ValueError("usuario no existe")
        return r[0]

    def listar(self):
        return self.repo.listar()
