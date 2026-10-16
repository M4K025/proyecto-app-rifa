# 01 — Diagrama de clases (dominio, pasado a limpio)

Unifica tus 3 hojas de cuaderno + `ComprarBoleta.xmi`.
Correcciones aplicadas: nombres consistentes, tipos explícitos, estados como `enum`, se eliminan duplicados (ej. `Compra`/`Pago` separados, `MetaRecaudacion` separada de `Rifa`).

```mermaid
classDiagram
  class Usuario {
    -int id
    -str nombre
    -str correo
    -str telefono
    -str documento
    -RolUsuario rol
    +registrar() void
    +iniciar_sesion() bool
    +actualizar() void
  }

  class Rifa {
    -int id
    -str titulo
    -str descripcion
    -float objetivo
    -float monto_recaudado
    -date fecha_inicio
    -date fecha_fin
    -EstadoRifa estado
    +crear() void
    +actualizar() void
    +verificar_meta() bool
    +listar_boletos_disponibles() list
  }

  class Boleto {
    -int id
    -int numero
    -float precio
    -EstadoBoleto estado
    -datetime fecha_apartado
    -int rifa_id
    -int comprador_id
    -int vendedor_id
    +reservar(comprador_id) void
    +marcar_vendido() void
    +liberar() void
  }

  class Compra {
    -int id
    -datetime fecha
    -float total
    -MetodoPago metodo_pago
    -EstadoCompra estado
    +calcular_total() float
    +confirmar() void
    +anular() void
  }

  class Pago {
    -int id
    -int compra_id
    -float monto
    -str referencia
    -datetime fecha
    -EstadoPago estado
    +aprobar() void
    +rechazar() void
  }

  class Sorteo {
    -int id
    -int rifa_id
    -datetime fecha_sorteo
    -int ganador_id
    -EstadoRifa estado
    +realizar_sorteo() int
  }

  class MetaRecaudacion {
    -int id
    -int rifa_id
    -float monto_meta
    -float monto_actual
    +actualizar_monto(valor) void
    +porcentaje() float
    +cumple_meta() bool
  }

  class Reporte {
    -int id
    -int rifa_id
    -datetime fecha_generacion
    -TipoReporte tipo
    +generar() void
    +exportar() str
  }

  class Comprobante {
    -int id
    -int compra_id
    -datetime fecha_emision
    -str codigo_qr
    +enviar_por_correo() void
  }

  Usuario "1" --> "0..*" Compra : realiza
  Compra "1" --> "1..*" Boleto : incluye
  Boleto "0..*" --> "1" Rifa : perteneceA
  Compra "1" --> "1" Comprobante : genera
  Compra "1" --> "1..*" Pago : tiene
  Rifa "1" --> "0..1" Sorteo : define
  Rifa "1" --> "0..1" MetaRecaudacion : controla
  Rifa "1" --> "0..*" Reporte : origina
```

## Enums (no los dibujaste, pero los usabas en texto)

- `RolUsuario`: ADMIN, ORGANIZADOR, VENDEDOR, CLIENTE
- `EstadoRifa`: ACTIVA, FINALIZADA, CANCELADA
- `EstadoBoleto`: DISPONIBLE, APARTADO, PAGADO, VENDIDO, RECHAZADO
- `EstadoCompra`: PENDIENTE, CONFIRMADA, ANULADA
- `MetodoPago`: EFECTIVO, TRANSFERENCIA, TARJETA, PSE
- `EstadoPago`: PENDIENTE, APROBADO, RECHAZADO
- `TipoReporte`: CUENTAS, RECAUDACION, BOLETOS

## Decisiones de sentido

1. `Boleto` no guarda `total`; `Compra.calcular_total()` lo deriva (evita inconsistencia).
2. `Pago` separado de `Compra`: una compra puede tener varios intentos de pago.
3. `Sorteo` y `MetaRecaudacion` separados de `Rifa` (principio responsabilidad única).
4. `Comprobante` (caso Comprar Boleta) ≠ `Reporte` (cierre administrativo).
