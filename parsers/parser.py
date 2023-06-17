from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# Шлях до веб-драйвера Chrome
webdriver_path = '../webdriver/chromedriver.exe'

# Налаштування параметрів веб-драйвера Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Запуск у фоновому режимі
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Створення екземпляра веб-драйвера Chrome
driver = webdriver.Chrome(service=Service(webdriver_path), options=chrome_options)

url = 'https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/'
driver.get(url)

# Очікування завантаження контенту (можливо, потрібно змінити дані параметри затримки)
driver.implicitly_wait(5)

# Отримання HTML-коду сторінки
html = driver.page_source

# Закриття веб-драйвера
driver.quit()

# Створення об'єкта BeautifulSoup для парсингу HTML-коду
soup = BeautifulSoup(html, 'html.parser')

div_parent_elements = soup.find_all('div', class_='MuiBox-root css-pw3923')

results = []

for parent_div in div_parent_elements:
    div_elements = parent_div.find_all('div', class_='MuiBox-root css-ieznkm')

    for div in div_elements:
        tariff_name_element = div.find('a', class_='MuiTypography-h3')
        tariff_name = tariff_name_element.text.strip() if tariff_name_element else None

        tariff_name_element = div.find('a', class_='MuiTypography-h3')
        tariff_href = tariff_name_element['href'] if tariff_name_element else None

        tariff_price_element = div.find('span', class_='MuiTypography-text5')
        tariff_price = tariff_price_element.text.strip() if tariff_price_element else None

        tariff_internet_elements = div.find_all('h5', class_='MuiTypography-text5')
        tariff_internet = tariff_internet_elements[0].text.strip() if tariff_internet_elements else None

        tariff_mins = tariff_internet_elements[1].text.strip() if len(tariff_internet_elements) > 1 else None

        social_bezlim_element = div.find('p', class_='MuiTypography-text5')
        social_bezlim = social_bezlim_element.text.strip() if social_bezlim_element else None

        result = {
            'Tariff name': tariff_name,
            'Tariff href': tariff_href,
            'Tariff price': tariff_price,
            'Tariff internet': tariff_internet,
            'Tariff mins': tariff_mins,
            'Social bezlim': social_bezlim
        }

        results.append(result)

with open('../tariffs.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print("Парсинг завершено і дані збережено у файлі tariffs.json.")