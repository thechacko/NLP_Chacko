
virtual_env:
	@python -m venv venv
	@.\venv\Scripts\activate.bat
	@.\venv\Scripts\python.exe -m pip install --upgrade pip
	@echo "Virtual environment created..."

install:
	pip install --no-cache-dir fastapi
	pip list
