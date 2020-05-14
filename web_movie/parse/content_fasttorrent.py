import csv
from bs4 import BeautifulSoup

from db import db
from web_movie import create_app
from web_movie.parse.url_fasttorrent import get_html
from web_movie.video.models import Film


def kino_scrap():
    """Парсинг данных со страницы фильма и сохранение в базу данных"""
    x = 0
    film_without_content = Film.query.filter(Film.img.is_(None))
    for film in film_without_content:
        country, producer, actors, operator, music_author, content, img = '', '', '', '', '', '', ''
        html = get_html(f'http://fast-torrent.ru{film.film_page}')
        if html:
            x += 1
            try:
                soup = BeautifulSoup(html, 'html.parser')
                content_films = soup.find('td', class_="info").find('div')
                country = []
                for i in content_films('a'):
                    if i.find('em', class_='cn-icon'):
                        country.append(i.find('em', class_='cn-icon')['title'])
                    country_formated = ', '.join(country)

                for prod in content_films('p', align='left'):
                    if "Режиссер" in prod.find('strong'):
                        producer = prod.find('a').text
                    elif "В ролях" in prod.find('strong'):
                        actors = []
                        for i in prod.find_all('a'):
                            actors.append(i.text)
                        actors_formated = ', '.join(actors)
                    elif "Оператор" in prod.find('strong'):
                        operator = prod.find('a').text
                    elif "Композитор" in prod.find('strong'):
                        music_author = prod.find('a').text
                content = content_films.find('p', class_='justify').text
                img = soup.find('a', class_='slideshow1')['href']
                print(x, country_formated, producer, actors_formated, operator, music_author, content, img)
                film.country = country_formated
                film.producer = producer
                film.actors = actors_formated
                film.operator = operator
                film.music_author = music_author
                film.content = content
                film.img = img
                db.session.add(film)
                db.session.commit()
            except:
                print('Ошибка')


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        kino_scrap()

