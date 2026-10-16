# PRODUCTO FINAL — Rifa App (POO 4 capas: FRONTEND · API · BACK · ORM)

Meta del negocio: **$2.000.000**.

## Qué enviar a tus compañeros (4 esquemas + código)

```
esquemas/E01_arquitectura_4capas.svg   -> arquitectura FRONTEND->API->BACK->ORM
esquemas/E02_clases_4capas.svg         -> clases por capas (BACK dominio + ORM tablas)
esquemas/E03_casos_uso_4capas.svg      -> casos de uso por capas
esquemas/E04_actividad_4capas.svg      -> actividad Comprar con carriles por capa
ENTREGA_Revision.html                  -> dossier bonito morado pastel (imprimible)
src/                                   -> aplicación COMPLETA (corre con SQLite)
```

Los 4 SVG se abren en navegador/WhatsApp/correo sin instalar nada.

## Capas (según clase POO)

| Capa | Carpeta | Contiene |
|------|---------|----------|
| FRONTEND | `src/rifa_app/frontend/` | `app_cli.py` menú completo + spec pantallas móvil |
| API | `src/rifa_app/api/` | `contratos.py` DTOs + `controladores.py` Api (8 endpoints) |
| BACK | `src/rifa_app/back/` | `dominio/` 8 entidades + enums · `servicios/` 7 servicios con reglas |
| ORM | `src/rifa_app/orm/` | `database.py` SQLite + `repositorios.py` 9 repos (fila<->objeto) |

Regla: FRONTEND solo llama API. API delega a BACK. BACK no escribe SQL. ORM no tiene reglas.

## Cómo correr

```powershell
# Prueba automática final (SQLite en memoria):
python ./src/test_final.py

# App completa (guarda en rifa.db):
python ./src/app.py

# Demo rápida:
python ./src/main_demo.py
```

Todo verificado el 16/10/2026: `OK producto final: rifa+compra+pago+reporte+sorteo con ORM SQLite`.
