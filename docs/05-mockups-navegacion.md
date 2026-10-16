# 05 — Mockups y navegación (pasados a limpio)

Tus fotos de cuaderno, ordenadas sin cambiar la idea:

```mermaid
flowchart TB
  REG[Registro: Registrarse / Crear] --> CREAR[Crear: Foto + ORM + Organizador + Info sorteo]
  REG --> APARTAR[Registrarse a rifa: #1 #2 #3]
  APARTAR --> DETALLE[# N: ORM personales]
  DETALLE --> ORM[Nombre · Teléfono · Correo · Nº Rifa · Estado: Pagado/Apartado/Rechazado]
  CREAR --> FICHA[Ficha premio: nombre, tamaño, usado Sí/No, color, contacto, organizador]
  FICHA --> INFO[Info sorteo: precio, fecha/hora, cantidad, disponible/reservado/pagado]
  INFO --> TABLERO[Tablero números: Apartar / Reservar / Pagar]
  TABLERO --> PAGAR[Pagar: nombre, correo, teléfono, documento, método, estado pendiente/aprobado]
```

## Pantallas (qué lleva cada una)

1. **Registro**: dos botones — `Registrarse` (cliente) / `Crear` (organizador).
2. **Crear rifa (organizador)**: Foto/video + ORM objeto (nombre, tamaño, color, usado, contacto) + Info sorteo (precio, fecha/hora, cantidad).
3. **Catálogo / Ficha**: foto premio + datos + contador (disponibles / apartados / pagados).
4. **Tablero de números**: grilla 00-99, colores por `EstadoBoleto`.
5. **Apartar/Pagar**: formulario (nombre, correo, teléfono, documento, método) → estado PENDIENTE → APROBADO/RECHAZADO.
6. **Mis rifas**: participadas (#apartado, #pagado, #rechazado) + creadas (activa/finalizada/cancelada).

Tu mapa a mano que decía `Rifados → Usuario/Registro | Organizador/fotos/orm/sorteo` es exactamente este flujo.
