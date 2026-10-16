# 02 — Arquitectura 4 capas: FRONTEND · API · BACK · ORM

```mermaid
flowchart TB
  FE["🟠 FRONTEND<br/>App móvil / CLI<br/>src/rifa_app/frontend/"]
  API["🌸 API<br/>REST DTOs + endpoints<br/>src/rifa_app/api/"]
  BACK["💜 BACK<br/>servicios + dominio<br/>src/rifa_app/back/"]
  DAT["🔵 ORM<br/>repositorios + BD<br/>src/rifa_app/orm/"]
  DB[(Base de datos)]

  FE --> API
  API --> BACK
  BACK --> DAT
  DAT --> DB

  style FE fill:#FFF7ED,stroke:#FB923C,stroke-width:2px
  style API fill:#FFE4E6,stroke:#F472B6,stroke-width:2px
  style BACK fill:#EDE9FE,stroke:#7C5CBF,stroke-width:2.5px
  style DAT fill:#DBEAFE,stroke:#60A5FA,stroke-width:2px
  style DB fill:#EDE9FE,stroke:#7C5CBF
```

| Capa | Carpeta | Contiene | Puede llamar | Prohibido |
|------|---------|----------|--------------|-----------|
| FRONTEND | `frontend/` | pantallas, CLI demo | API | BACK/ORM directo |
| API | `api/` | `contratos.py`, `post_compras()` | BACK servicios | SQL, UI |
| BACK | `back/dominio/` + `back/servicios/` | entidades + reglas | interfaces ORM | HTTP, SQL |
| ORM | `orm/` | `RepositorioMemoria` → SQLite | dominio | servicios, UI |

> Ver versión bonita lista para revisión: `../ENTREGA_Revision.html` (morado pastel, imprimible).
