# Crear entorno virtual
venv:
	@test -d .venv || uv venv

# Instalar dependencias
install: venv
	@if [ -f pyproject.toml ]; then \
	    echo "Usando pyproject.toml con uv sync --dev"; \
	    uv sync --dev; \
	else \
	    echo "Instalando desde requirements.txt"; \
	    if [ -f requirements.txt ]; then uv pip install -r requirements.txt; fi; \
	fi

# Ejecutar servidor en modo desarrollo
run-dev:
	@echo "Iniciando servidor de desarrollo en http://localhost:3000"
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 3000

# Ejecutar servidor en modo producción
run-pro:
	@echo "Iniciando servidor de producción en http://localhost:3000"
	uv run uvicorn main:app --host 0.0.0.0 --port 3000

# Formatear código
format:
	@echo "Formateando con Ruff"
	uv run ruff format agentes api config services


# Lint
lint:
	@echo "Ejecutando análisis con Ruff"
	uv run ruff check agentes api config services


# Lint con autofix
lint-fix:
	@echo "Analizando y corrigiendo con Ruff"
	uv run ruff check agentes api config services --fix

# Refactorización rápida
refactor: format lint

# Limpiar archivos generados
clean:
	@echo "Limpiando archivos generados"
	rm -rf .venv .pytest_cache .ruff_cache .coverage htmlcov \
	    build dist *.egg-info **/*.egg-info __pycache__ **/__pycache__

# Ejecutar todo el flujo
all: install format lintv