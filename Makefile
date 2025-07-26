# Disk Usage Analyzer - Makefile

.PHONY: help install install-dev test clean run-cli run-web example lint format

# Default target
help:
	@echo "🔍 Disk Usage Analyzer - Comandos Disponíveis"
	@echo "=============================================="
	@echo "install      - Instalar o pacote"
	@echo "install-dev  - Instalar com dependências de desenvolvimento"
	@echo "test         - Executar testes"
	@echo "clean        - Limpar arquivos temporários"
	@echo "run-cli      - Executar interface CLI"
	@echo "run-web      - Executar interface web"
	@echo "example      - Executar exemplo"
	@echo "lint         - Verificar código com flake8"
	@echo "format       - Formatar código com black"
	@echo "build        - Construir pacote para distribuição"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e .[dev]
	pip install -r requirements.txt

# Testing
test:
	python -m pytest tests/ -v --cov=src

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

# Running
run-cli:
	python src/cli/main.py --help

run-web:
	python src/web/app.py --host 0.0.0.0 --port 8080

example:
	python example.py

# Code quality
lint:
	flake8 src/ --max-line-length=100 --ignore=E203,W503

format:
	black src/ --line-length=100
	black example.py --line-length=100

# Building
build: clean
	python setup.py sdist bdist_wheel

# Quick analysis commands
analyze-home:
	python src/cli/main.py /home --min-size 1MB --max-depth 3

analyze-var:
	python src/cli/main.py /var --min-size 10MB --max-depth 2

analyze-current:
	python src/cli/main.py . --tree-items 15

# Development server
dev-web:
	python src/web/app.py --debug --host 127.0.0.1 --port 5000

# Install and run
quick-start: install example

# Full setup for development
setup-dev: install-dev
	@echo "✅ Ambiente de desenvolvimento configurado!"
	@echo "Execute 'make run-web' para iniciar a interface web"
	@echo "Execute 'make example' para ver um exemplo de uso"
