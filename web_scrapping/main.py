import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/articles/'
BASE_URL = 'https://habr.com'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        title_tag = article.find('h2')
        if not title_tag:
            continue

        link_tag = title_tag.find('a')
        if not link_tag:
            continue

        time_tag = article.find('time')
        if not time_tag:
            continue

        title = link_tag.text.strip()
        href = link_tag.get('href')
        link = BASE_URL + href if href.startswith('/') else href
        date = time_tag.get('datetime')

        preview_text = article.get_text(separator=' ', strip=True).lower()

        if any(keyword.lower() in preview_text for keyword in KEYWORDS):
            print(f'{date} – {title} – {link}')

except requests.exceptions.RequestException as error:
    print(f'Ошибка при выполнении запроса: {error}')
