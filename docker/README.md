#  Docker - Sistema de Agentes Inteligentes

Esta carpeta contiene toda la configuración de Docker para ejecutar la aplicación y su base de datos.

# Archivos

- `Dockerfile`: Define la imagen de la aplicación FastAPI
- `docker-compose.app.yml`: Orquesta el contenedor de la app
- `docker-compose.db.yml`: Orquesta el contenedor de PostgreSQL
- `.dockerignore`: Archivos a excluir del build (crear en raíz si es necesario)

## Uso Rápido

Desde la **raíz del proyecto**:

```bash
# 1. Levantar base de datos
docker compose -f docker/docker-compose.db.yml up -d

# 2. Levantar aplicación
docker compose -f docker/docker-compose.app.yml up -d
```

## Comandos Útiles

```bash
# Ver logs de la app
docker compose -f docker/docker-compose.app.yml logs -f

# Ver logs de la BD
docker compose -f docker/docker-compose.db.yml logs -f

# Estado de servicios
docker compose -f docker/docker-compose.app.yml ps
docker compose -f docker/docker-compose.db.yml ps

# Detener servicios
docker compose -f docker/docker-compose.app.yml down
docker compose -f docker/docker-compose.db.yml down

# Limpiar todo (incluyendo BD)
docker compose -f docker/docker-compose.db.yml down -v
```

## Configuración

Antes de levantar los servicios:

1. Tener `.env` en la **raíz** del proyecto con tus variables de entorno (OPENAI_API_KEY, etc.)
2. Tener Docker y Docker Compose instalados

La variable `POSTGRES_CONNECTION_STRING` en `.env` debe apuntar a:
- `postgresql://postgres:admin@host.docker.internal:5433/agentes_db` (si BD en contenedor desde app en contenedor)
- `postgresql://postgres:admin@localhost:5433/agentes_db` (si BD local o en host)

## Para más detalles

Ver la documentación completa en `../DOCKER.md`
