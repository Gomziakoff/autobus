import requests
from bs4 import BeautifulSoup
import json
import re
import execjs
import time

url = 'https://ru.busti.me/brest/stop/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    containers = soup.find_all('div', class_='ui fluid vertical menu')  # замените 'container' на нужный класс
    hrefs = []
    for container in containers:
        a_tags = container.find_all('a', class_='item')
        for a in a_tags:
            hrefs.append(a.get('href'))

    print(hrefs)
    astops_dict = {}
    for url in hrefs:
        url = 'https://ru.busti.me' + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.find('head')
        script = container.find('script', type="text/javascript", src="")
        time.sleep(1)
        if script:
            print(url)
            text = script.text
            # Используем регулярное выражение для извлечения данных об остановках
            pattern = r'\b(\d+):\s*{([^}]*)}'
            matches = re.findall(pattern, text)

            for match in matches:
                stop_id = match[0]
                stop_data = match[1]
                stop_info = {}
                # Разбиваем данные об остановке на отдельные элементы
                stop_items = re.findall(r'(\w+):\s*("[^"]*"|\b\d+\.\d+\b|\b\d+\b)', stop_data)
                for item in stop_items:
                    key = item[0]
                    value = item[1].strip('"')
                    if key not in ['id', 'tram_only']:  # Исключаем ключи "id" и "tram_only"
                        stop_info[key] = value
                astops_dict[stop_id] = stop_info
            # Преобразуем словарь в список словарей
        else:
            print(url,"error")
    astops_list = []
    for stop_id, stop_info in astops_dict.items():
        astops_list.append(stop_info)

    # Записываем данные в JSON-файл
    with open('astops.json', 'w', encoding='utf-8') as f:
        json.dump(astops_list, f, ensure_ascii=False, indent=4)

