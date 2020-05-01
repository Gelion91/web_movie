from bs4 import BeautifulSoup

from db import db
from web_movie import create_app
from web_movie.parse.url_fasttorrent import get_html
from web_movie.parse.ya_api import get_response
from web_movie.video.models import Film


app = create_app()
with app.app_context():
    def get_rating_page(x):
        result = get_html(f'https://rating.kinopoisk.ru/{x}.xml')
        if result:
            soup = BeautifulSoup(result, 'html.parser')
            kp_rating = soup.find('kp_rating').text
            return kp_rating
        return ''


    def get_ratio():
        film_without_rating = Film.query.filter(Film.rating.is_(None))
        for film in film_without_rating:
            if film.kino_id:
                rating = get_rating_page(film.kino_id)
                film.rating = rating
                print(rating)
                db.session.add(film)
                db.session.commit()

    get_ratio()