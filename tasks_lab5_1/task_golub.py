import requests
from bs4 import BeautifulSoup
import re
url = "https://ru.wikipedia.org/wiki/Голубь"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
content = soup.find('div', {'class': 'mw-parser-output'})
first_p = content.find('p', recursive=False)
summary = re.sub(r'\[.*?\]', '', first_p.text)
summary = summary.replace('\n', '').strip()
print(f"Общая характеристика: {summary}")