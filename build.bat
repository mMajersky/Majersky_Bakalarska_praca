@echo off
echo 🔁 Rebuilding venv...

:: Zmažeme starý venv (ak existuje)
rmdir /s /q venv

:: Vytvoríme nový venv
python -m venv venv

:: Aktivujeme venv
call venv\Scripts\activate

:: Nainštalujeme knižnice z requirements.txt
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Zmažeme staré buildy
rmdir /s /q build
rmdir /s /q dist
del /q *.spec

echo 🛠️ Building EXE files...

:: Build menu.py
pyinstaller --onefile --noconsole ^
  --add-data "assets;assets" ^
  --add-data "lvls;lvls" ^
  --add-data "scripts;scripts" ^
  --additional-hooks-dir=pyi-hooks menu.py


:: Build editor_menu.py
pyinstaller --onefile --noconsole ^
  --add-data "assets;assets" ^
  --add-data "lvls;lvls" ^
  --add-data "scripts;scripts" ^
  --additional-hooks-dir=pyi-hooks editor_menu.py




:: Skopírujeme assets, lvls, scripts do dist/
echo 📁 Copying folders...
xcopy lvls dist\lvls\ /E /I /Y
xcopy assets dist\assets\ /E /I /Y
xcopy scripts dist\scripts\ /E /I /Y

:: Skopírujeme aj herné režimy do dist/
copy /Y platformer.py dist\
copy /Y prototype.py dist\
copy /Y sokoban.py dist\
copy /Y editor.py dist\

echo ✅ Build complete! EXE súbory + dáta sú pripravené v dist\
pause
