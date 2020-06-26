from db import db
from web_movie import create_app
from web_movie.parse.ya_api import get_response
from web_movie.video.models import Film


app = create_app()
with app.app_context():
    def get_film_id():
        film_without_id = Film.query.filter(Film.kino_id.is_(None))
        for film in film_without_id:
            if film.producer:
                print(film.year.split('.')[-1], film.name, film.producer)
                result = get_response(film.name, producer=film.producer)
                if result:
                    if not Film.query.filter(Film.kino_id == result).first():
                        film.kino_id = result
                        db.session.add(film)
                        db.session.commit()
