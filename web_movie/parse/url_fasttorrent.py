import csv
import requests
from bs4 import BeautifulSoup

from web_movie import db
from web_movie.video.models import Film
from fake_useragent import UserAgent


def get_html(url):
    try:
        session = requests.Session()
        result = session.get(url, headers={'User-Agent': UserAgent().chrome})
        print(session.cookies)
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def scrap_filmlist(x):
    """Паринг ссылок на страницы с фильмами"""
    html = get_html(f'http://fast-torrent.ru/new-films/{x}.html')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_films = soup.find('div', class_="film-list").findAll('div', itemtype='https://schema.org/Movie')
        print(x)
        film_list = []
        for film in all_films:
            name = film.find('div', class_='film-image')['alt']
            url = film.find('div', class_='film-image').find('a')['href']
            print(name, url)
            film_list.append({'name': name, 'url': url})

        with open('url_fasttorrent.csv', 'a+', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            writer.writerow(('name', 'url'))
            for film in film_list:
                writer.writerow((film['name'], film['url']))


def save_video(img, name, category, kino_id):
    new_video = Film.query.filter(Film.img == img).count()
    if not new_video:
        new_video = Film(img=img, name=name, category=category, kino_id=kino_id, content='', film_page='', year='')
        db.session.add(new_video)
        db.session.commit()


if __name__ == "__main__":
    for x in range(1, 3013):
        scrap_filmlist(x)
