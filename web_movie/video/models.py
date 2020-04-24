from db import db


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(), index=True)
    img = db.Column(db.String(), index=True, unique=True)
    name = db.Column(db.String(), index=True)
    category = db.Column(db.String(), index=True)
    kino_id = db.Column(db.String(), index=True, unique=True)
    content = db.Column(db.String())
    film_page = db.Column(db.String())

    def __repr__(self):
        return f'фильм {"name"}, id: {"id"}'
