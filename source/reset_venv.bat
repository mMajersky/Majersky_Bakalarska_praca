@echo off
echo 🔁 Removing old virtual environment...
rmdir /s /q venv

echo 🧱 Creating new virtual environment...
python -m venv venv

echo 🔄 Activating virtual environment...
call venv\Scripts\activate

echo 📦 Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 🧪 Verifying pygame import...
python -c "import pygame; print('✅ pygame version:', pygame.__version__); print('✅ SDL version:', pygame.get_sdl_version()); print('✅ Has Surface:', hasattr(pygame, 'Surface')); print('✅ Has init:', hasattr(pygame, 'init'))"

pause
