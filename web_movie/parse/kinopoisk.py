import requests
from bs4 import BeautifulSoup

from web_movie import db
from web_movie.video.models import Film
from fake_useragent import UserAgent


# proxies = []
# with open('get.json', 'r', encoding='utf-8') as f:
#     result = json.loads(f.read())
#     for name in result.values():
#         try:
#             print(name['name'])
#             proxies.append({'http': name['name']})
#         except TypeError:
#             pass

# print(proxies)


def get_html(url):
    try:
        print(UserAgent().ie)
        session = requests.Session()
        result = session.get(url, headers={'User-Agent': UserAgent().chrome})
        print(session.cookies)
        result.raise_for_status()
        if "div_usa_box_td1" in result.text:
            return result.text

    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def kino_scrap(query):
    html = get_html(f'https://www.kinopoisk.ru/film/{query}')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find('img', itemprop="image")['src']
        name = soup.find('h1', class_="moviename-big").text.lower().strip()
        category = soup.find('span', itemprop="genre").text.lower()
        kino_id = query
        save_video(img, name, category, kino_id)


def save_video(img, name, category, kino_id):
    new_video = Film.query.filter(Film.img == img).count()
    if not new_video:
        new_video = Film(img=img, name=name, category=category, kino_id=kino_id, content='', film_page='', year='')
        db.session.add(new_video)
        db.session.commit()


