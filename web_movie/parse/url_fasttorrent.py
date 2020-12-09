import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from web_movie import db, create_app
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
        for film in all_films:
            try:
                name = film.find('div', class_='film-image')['alt']
                try:
                    alternative_name = film.find('div', class_='film-wrap').find('span', itemprop="alternativeHeadline").text
                    print(alternative_name)
                except:
                    alternative_name = None
                url = film.find('div', class_='film-image').find('a')['href']
                year = film.find('div', class_='film-foot').find('em').text
                year = year.split(' ')[-1]
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
                    alternative_name=alternative_name,
                    category=category,
                    year=year,
                    published=datetime.strptime(year, '%d.%m.%Y'),
                    film_page=url)
                db.session.add(new_video)
                db.session.commit()


def add_alt_name():
    x = 0
    film_without_content = Film.query.filter(Film.alternative_name.is_(None))
    for film in film_without_content:
        html = get_html(f'http://fast-torrent.ru{film.film_page}')
        if html:
            x += 1
            soup = BeautifulSoup(html, 'html.parser')
            try:
                alternative_name = soup.find('span', itemprop="alternativeHeadline").text
            except:
                alternative_name = None

            film.alternative_name = alternative_name
            print(film.alternative_name)
            db.session.add(film)
            db.session.commit()

def kino_scrap():
    """Парсинг данных со страницы фильма и сохранение в базу данных"""
    x = 0
    film_without_content = Film.query.filter(Film.content.is_(None))
    for film in film_without_content:
        country, producer, actors, operator, music_author, content, img = '', '', '', '', '', '', ''
        html = get_html(f'http://fast-torrent.ru{film.film_page}')
        if html:
            x += 1
            try:
                soup = BeautifulSoup(html, 'html.parser')
                content_films = soup.find('td', class_="info").find('div')

                try:
                    alternative_name = soup.find('span', itemprop="alternativeHeadline").text
                except:
                    alternative_name = None

                country = []
                for i in content_films('a'):
                    if i.find('em', class_='cn-icon'):
                        country.append(i.find('em', class_='cn-icon')['title'])
                country_formated = ', '.join(country)

                actors = []
                for prod in content_films('p', align='left'):
                    if "Режиссер" or "Режиссеры" in prod.find('strong'):
                        producer = prod.find('a').text
                        print('Producer: ', producer)
                    elif "В ролях" in prod.find('strong'):
                        for i in prod.find_all('a'):
                            actors.append(i.text)
                    elif "Оператор" in prod.find('strong'):
                        operator = prod.find('a').text
                    elif "Композитор" in prod.find('strong'):
                        music_author = prod.find('a').text
                actors_formated = ', '.join(actors)
                try:
                    content = content_films.find('p', class_='justify').text
                except Exception as s:
                    print("Контент: ", s)

                img = soup.find('a', class_='slideshow1')['href']
                print(x, country_formated, producer, actors_formated, operator, music_author, content, img)
                film.country = country_formated
                film.producer = producer
                film.actors = actors_formated
                film.operator = operator
                film.music_author = music_author
                film.content = content
                film.img = img
                film.alternative_name = alternative_name
                print("add producer:", film.producer)
                db.session.add(film)
                db.session.commit()
            except Exception as s:
                print('Ошибка: ', s)


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
            print(x)
        kino_scrap()
        add_alt_name()
        get_film_id()

