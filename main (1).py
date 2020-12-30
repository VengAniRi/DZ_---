import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_TIME, '')

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

r = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(r.text, 'html.parser')
articles = soup.find_all('article', class_='post post_preview')

for article in articles:
    title = article.find('a', class_='post__title_link')
    text = article.find('div', class_='post__text-html').text
    tags_list = article.find_all('a', class_=['inline-list__item-link', 'hub-link'])
    tags = ' '.join([tag.text for tag in tags_list])

    info = ' '.join([title.text, text, tags]).lower()
    if any(kw in info for kw in KEYWORDS):
        date = article.find('span', class_='post__time').text
        if 'сегодня' in date:
            date = datetime.today()
        elif 'вчера' in date:
            date = datetime.today() - timedelta(days=1)
        else:
            d, m, y = date.split()[:3]
            m = m[:3]
            date = datetime.strptime(' '.join([d, m, y]), '%d %b %Y')
        date = date.strftime('%d.%m.%Y')
        link = title['href']
        print(f'{date} - {title.text} - {link}')
