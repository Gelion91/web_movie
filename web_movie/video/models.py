from db import db


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    published = db.Column(db.DateTime)
    year = db.Column(db.String(), index=True)
    img = db.Column(db.String(), index=True, unique=True)
    name = db.Column(db.String(), index=True)
    name_lower = db.Column(db.String(), index=True)
    category = db.Column(db.String(), index=True)
    tags = db.Column(db.String(), index=True)
    kino_id = db.Column(db.String(), index=True, unique=True)
    content = db.Column(db.String())
    producer = db.Column(db.String(), index=True)
    film_page = db.Column(db.String())
    actors = db.Column(db.String(), index=True)
    writers = db.Column(db.String(), index=True)
    operator = db.Column(db.String(), index=True)
    music_author = db.Column(db.String(), index=True)
    country = db.Column(db.String(), index=True)
    rating = db.Column(db.String(), index=True)

    def __repr__(self):
        return f'фильм {"name"}, id: {"id"}'


class Serials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    published = db.Column(db.DateTime)
    year = db.Column(db.String(), index=True)
    img = db.Column(db.String(), index=True, unique=True)
    name = db.Column(db.String(), index=True)
    name_lower = db.Column(db.String(), index=True)
    category = db.Column(db.String(), index=True)
    tags = db.Column(db.String(), index=True)
    kino_id = db.Column(db.String(), index=True, unique=True)
    content = db.Column(db.String())
    producer = db.Column(db.String(), index=True)
    film_page = db.Column(db.String())
    actors = db.Column(db.String(), index=True)
    writers = db.Column(db.String(), index=True)
    operator = db.Column(db.String(), index=True)
    music_author = db.Column(db.String(), index=True)
    country = db.Column(db.String(), index=True)
    rating = db.Column(db.String(), index=True)

    def __repr__(self):
        return f'Сериал {"name"}, id: {"id"}'