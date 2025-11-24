import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import sys
import re


def load_page(country, cache_dir="cache"):
    """Загружает страницу из кэша или интернета."""
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Нормализуем имя файла
    filename = country.replace(" ", "_") + ".html"
    file_path = os.path.join(cache_dir, filename)

    # 1. Пробуем загрузить из кэша
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content:  # Проверка на пустой файл
                return content

    # 2. Если нет в кэше, качаем
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        print(f"Загрузка: {url}")
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        html = r.text

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        time.sleep(1)  # Вежливость
        return html

    except Exception as e:
        print(f"Ошибка при загрузке {country}: {e}")
        return None


def clean_text(text):
    """Удаляет мусорные символы."""
    if not text:
        return ""
    # Заменяем все виды пробелов на обычный
    text = re.sub(r'\s+', ' ', text)
    # Удаляем сноски [1], [note 1]
    text = re.sub(r'\[.*?\]', '', text)
    # Удаляем содержимое круглых скобок, если это не часть названия (упрощение)
    # Часто там (2024 est.) или (approx)
    text = re.sub(r'\(.*?\)', '', text)
    return text.strip()


def extract_numbers_from_text(text):
    """Возвращает список всех найденных чисел (float) в тексте."""
    # 1. Склеиваем пробелы между цифрами: "84 000 000" -> "84000000"
    # Регулярка ищет: цифра + пробел + цифра
    clean_spaces = re.sub(r'(?<=\d)\s(?=\d)', '', text)

    # 2. Удаляем запятые (разделители тысяч)
    clean_commas = clean_spaces.replace(',', '')

    # 3. Ищем все последовательности цифр (возможно с точкой)
    # Игнорируем одиночные цифры, чтобы не ловить сноски, если они остались
    matches = re.findall(r'(\d+(?:\.\d+)?)', clean_commas)

    numbers = []
    for m in matches:
        try:
            val = float(m)
            numbers.append(val)
        except ValueError:
            continue
    return numbers


def parse_infobox(html):
    if not html:
        return "N/A", "N/A", "N/A"

    soup = BeautifulSoup(html, "html.parser")

    # Ищем таблицу с классом, содержащим 'infobox' (более надежно)
    box = soup.find("table", {"class": re.compile("infobox")})
    if not box:
        return "N/A", "N/A", "N/A"

    # --- ОЧИСТКА DOM ---
    # Удаляем ненужные теги, которые мешают парсингу текста
    for tag in box.find_all(['sup', 'style', 'script', 'span']):
        # span удаляем только если это flagicon или display:none
        if tag.name == 'span' and ('flagicon' in tag.get('class', []) or 'display:none' in tag.get('style', '')):
            tag.decompose()
        elif tag.name in ['sup', 'style', 'script']:
            tag.decompose()

    capital = "N/A"
    area_candidates = []
    pop_candidates = []

    rows = box.find_all("tr")

    # Флаги сканирования
    scan_area = 0
    scan_pop = 0

    for i, row in enumerate(rows):
        text_row = clean_text(row.get_text(" "))
        header = row.find("th")
        header_text = clean_text(header.get_text(" ")) if header else ""

        # --- 1. СТОЛИЦА ---
        if "Capital" in header_text and capital == "N/A":
            td = row.find("td")
            if td:
                # Приоритет: ссылка <a>
                link = td.find("a")
                if link:
                    capital = link.get_text(strip=True)
                else:
                    # Иначе текст. Берем все до первой цифры (чтобы отсечь координаты)
                    cap_text = clean_text(td.get_text())
                    # Часто бывает "Berlin 52°N..." -> берем "Berlin"
                    # Разбиваем по ; или координатам
                    capital = re.split(r'[;,\d]', cap_text)[0].strip()

        # --- 2. ПЛОЩАДЬ (Запуск сканера) ---
        if "Area" in header_text and "code" not in header_text:  # Исключаем "Area code"
            scan_area = 5  # Сканируем эту строку + 4 следующих

        if scan_area > 0:
            # Если встретили "Population", "GDP", прекращаем сканировать Area
            if "Population" in header_text or "GDP" in header_text:
                scan_area = 0
            else:
                nums = extract_numbers_from_text(text_row)
                area_candidates.extend(nums)
                scan_area -= 1

        # --- 3. НАСЕЛЕНИЕ (Запуск сканера) ---
        if "Population" in header_text and "Density" not in header_text:
            scan_pop = 5  # Сканируем эту строку + 4 следующих

        if scan_pop > 0:
            # Если встретили "GDP", "Gini", "HDI", прекращаем
            if "GDP" in header_text or "Gini" in header_text:
                scan_pop = 0
            else:
                nums = extract_numbers_from_text(text_row)
                pop_candidates.extend(nums)
                scan_pop -= 1

    # --- ФИНАЛЬНЫЙ ВЫБОР ---

    # Площадь: берем МАКСИМУМ.
    # Почему: км² обычно больше чем миль². Общая площадь больше чем площадь воды.
    final_area = "N/A"
    if area_candidates:
        max_area = max(area_candidates)
        if max_area > 0:
            final_area = str(int(max_area)) if max_area.is_integer() else str(max_area)

    # Население: берем МАКСИМУМ.
    # Почему: Население (миллионы) > Года (2023) > Плотности (100-1000).
    final_pop = "N/A"
    if pop_candidates:
        # Фильтр: население страны вряд ли меньше 1000 человек (отсекаем мелкие цифры, если есть большие)
        valid_pops = [x for x in pop_candidates if x > 2100]  # Больше чем текущий год
        if valid_pops:
            max_pop = max(valid_pops)
        else:
            max_pop = max(pop_candidates)  # Если только малые числа, берем что есть

        final_pop = str(int(max_pop)) if max_pop.is_integer() else str(max_pop)

    return capital, final_area, final_pop


def main():
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = "countries.txt"
        output_file = "countries_data.csv"

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден!")
        # Создадим его для теста
        with open(input_file, "w") as f:
            f.write("France\nBrazil\nJapan\nGermany\nRussia")
        print(f"Создан тестовый файл {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        countries = [line.strip() for line in f if line.strip()]

    results = []

    print(f"{'Страна':<10} | {'Столица':<15} | {'Площадь':<12} | {'Население':<15}")
    print("-" * 65)

    for country in countries:
        html = load_page(country)
        capital, area, pop = parse_infobox(html)

        print(f"{country:<10} | {capital:<15} | {area:<12} | {pop:<15}")
        results.append([country, capital, area, pop])

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["country", "city", "area", "population"])
        writer.writerows(results)

    print(f"\nГотово! Файл сохранен: {output_file}")


if __name__ == "__main__":
    main()