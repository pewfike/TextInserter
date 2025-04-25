@echo off
echo Building Text Inserter v2.0...

:: Create executable directly in current directory with Files directory included
python -m PyInstaller --onefile --windowed --add-data "Files;Files" --distpath . TextFileInserter.py

echo Build complete! Check for TextFileInserter.exe in the current directory
pause 