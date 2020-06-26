import csv
import requests
from bs4 import BeautifulSoup

from web_movie import db, create_app
from web_movie.parse.content_fasttorrent import *
from web_movie.parse.get_id import get_film_id
from web_movie.video.models import Film
from fake_useragent import UserAgent


def get_html(url):
    try:
        session = requests.Session()
        result = session.get(url, headers={'User-Agent': UserAgent().chrome})
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print(url)
        print("Сетевая ошибка")
        with open('trouble.txt', 'a+', encoding='utf-8') as file:
            file.write(url + '\n')


def scrap_filmlist(page):
    """Парсинг ссылок на страницы с фильмами"""
    html = get_html(f'http://fast-torrent.ru/new-films/{page}.html')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_films = soup.find('div', class_="film-list").findAll('div', itemtype='https://schema.org/Movie')
        print(x)
        for film in all_films:
            try:
                name = film.find('div', class_='film-image')['alt']
                url = film.find('div', class_='film-image').find('a')['href']
                year = film.find('div', class_='film-foot').find('em').text
            except AttributeError:
                print("C этим фильмом проблема!", name)
            genre = []
            for cat in film.find('div', class_='film-genre').find_all('a', itemprop='genre'):
                genre.append(cat.text)
            category = ', '.join(genre)
            print(name, url)
            new_video = Film.query.filter(Film.film_page == url).count()
            if not new_video:
                new_video = Film(
                    name=name,
                    name_lower=name.lower(),
                    category=category,
                    year=year.split(' ')[-1],
                    film_page=url)
                db.session.add(new_video)
                db.session.commit()


def save_video(img, name, category, kino_id):
    new_video = Film.query.filter(Film.img == img).count()
    if not new_video:
        new_video = Film(img=img, name=name, category=category, kino_id=kino_id, content='', film_page='', year='')
        db.session.add(new_video)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        for x in range(1, 10):
            scrap_filmlist(x)
        kino_scrap()
        get_film_id()

