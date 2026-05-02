.PHONY: help install run debug clean lint lint-strict

help:
	@echo "Targets disponibles:"
	@echo "  make install      - Installer les dépendances"
	@echo "  make run          - Exécuter le projet"
	@echo "  make debug        - Exécuter avec pdb"
	@echo "  make clean        - Nettoyer caches/fichiers temporaires"
	@echo "  make lint         - flake8 + mypy (flags obligatoires)"
	@echo "  make lint-strict  - flake8 + mypy --strict"

install:
	uv sync

run:
	uv run python srcs/a_maze_ing.py config.txt

debug:
	uv run python -m pdb srcs/a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict
