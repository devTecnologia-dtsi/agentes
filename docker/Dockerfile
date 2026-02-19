# Etapa 1: Build
# Instala y compila dependencias de Python.
# Algunas dependencias necesitan herramientas como gcc para instalarse.
# Deja listo todo lo necesario para copiarlo luego a una imagen final más liviana.
FROM python:3.13-slim AS builder

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno para optimización de Python
# Evitar buffering en la salida de Python para que los logs se muestren en tiempo real
# Evitar que Python escriba archivos .pyc
# Evitar cache de pip para reducir el tamaño de la imagen
# Evitar que pip revise actualizaciones de pip para acelerar la instalación
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copiar archivos de dependencias
COPY pyproject.toml ./

# Instalar uv y dependencias del proyecto
RUN pip install --upgrade pip uv && \
    uv pip install --system -e .

# Etapa 2: Runtime
# Crea la imagen final que se ejecuta en producción.
# Evita incluir herramientas de compilación y reduce tamaño/riesgos.
# Imagen más ligera, más rápida de descargar y más segura.
FROM python:3.13-slim

# Variables de entorno
# Evitar buffering en la salida de Python para que los logs se muestren en tiempo real
# Evitar que Python escriba archivos .pyc
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar solo las bibliotecas de runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios de la aplicación
RUN mkdir -p /app /app/logs

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde la etapa builder
COPY --from=builder /usr/local /usr/local

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto de la aplicación
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/status', timeout=3).read()"

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
