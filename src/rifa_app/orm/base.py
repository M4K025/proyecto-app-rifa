from typing import Generic, TypeVar
T = TypeVar('T')

class RepositorioMemoria(Generic[T]):

    def __init__(self) -> None:
        self._datos: dict[int, T] = {}
        self._seq = 1

    def guardar(self, obj: T) -> T:
        obj_id = getattr(obj, 'id', 0) or 0
        if obj_id in (0, None):
            setattr(obj, 'id', self._seq)
            self._seq += 1
        self._datos[obj.id] = obj
        return obj

    def obtener(self, obj_id: int) -> T | None:
        return self._datos.get(obj_id)

    def listar(self) -> list[T]:
        return list(self._datos.values())

    def eliminar(self, obj_id: int) -> None:
        self._datos.pop(obj_id, None)

    def buscar_por(self, **filtros) -> list[T]:
        out = []
        for o in self._datos.values():
            if all((getattr(o, k, None) == v for k, v in filtros.items())):
                out.append(o)
        return out
