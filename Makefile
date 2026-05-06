install:
	uv venv
	uv sync
run: install
	src/pacman/main.py