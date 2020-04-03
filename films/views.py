from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user
from web_movie import User
from web_movie.video.models import Film

blueprint = Blueprint('films', __name__, url_prefix='/films')


@blueprint.route('/<int:film_id>', methods=['POST', 'GET'])
def show_films(film_id):
    my_film = Film.query.filter_by(kino_id=film_id).first()
    print(my_film.name)
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        return render_template('films/show_film.html', page_title=my_film.name.capitalize(),username=username, film=my_film)