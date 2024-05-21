@echo off
REM Запуск установки библиотек
pip install -r requirements.txt > nul

REM Запуск Python скрипта
python main.py