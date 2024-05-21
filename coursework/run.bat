@echo off
REM Запуск другого установка библиотек
pip install -r requirements.txt > nul

REM Запуск Python скрипта
python main.py