import os
import pandas as pd
import shutil

def is_broken(file_path):
    try:
        df = pd.read_csv(file_path)
        # Проверка на наличие столбца "Время"
        if 'Время' not in df.columns:
            return True
        # Проверка на наличие значений в столбце "Время"
        if df['Время'].isnull().any():
            return True
        # Проверка, что в столбце "Время" только цифры
        if not df['Время'].astype(str).str.isnumeric().all():
            return True
        return False
    except Exception as e:
        # Если возникает ошибка при чтении файла, считаем его сломанным
        return True

def validate():
    source_folder = 'download/data/'  # замените на путь к папке с файлами
    broken_folder = os.path.join('download/', 'broken')

    # Создаем папку для сломанных файлов, если она не существует
    os.makedirs(broken_folder, exist_ok=True)

    for filename in os.listdir(source_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(source_folder, filename)
            if is_broken(file_path):
                shutil.move(file_path, os.path.join(broken_folder, filename))
