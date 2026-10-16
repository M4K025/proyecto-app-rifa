# 03 — Casos de uso (limpio)

## Actores
- **Cliente / Usuario**: compra y aparta boletos.
- **Organizador / Vendedor**: crea rifa, ve reportes.
- **PasarelaDePago**: actor secundario que valida el pago.

```mermaid
flowchart LR
  Cliente((Cliente))
  Org((Organizador))
  Pas((PasarelaDePago))

  UC1[Comprar Boleta]
  UC2[Seleccionar Rifa]
  UC3[Seleccionar Boleta]
  UC4[Realizar Pago]
  UC5[Generar Comprobante]
  UC6[Cancelar Compra]
  UC7[Crear Rifa]
  UC8[Generar Reporte]
  UC9[Realizar Sorteo]

  Cliente --> UC1
  UC1 -. <<include>> .-> UC2
  UC1 -. <<include>> .-> UC3
  UC1 -. <<include>> .-> UC4
  UC1 -. <<include>> .-> UC5
  UC6 -. <<extend>> .-> UC1
  Pas --> UC4
  Org --> UC7 & UC8 & UC9
```

Tu XMI ya trae esto para Modelio (`Comprar Boleta` + 4 includes + 1 extend). Aquí se agregan `Crear Rifa`, `Generar Reporte` y `Realizar Sorteo` que estaban en tus hojas pero faltaban en el XMI.
