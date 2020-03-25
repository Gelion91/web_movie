from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user
from web_movie import get_response, User
from .models import Film
from web_movie.parse.kinopoisk import kino_scrap
blueprint = Blueprint('search', __name__)


@blueprint.route('/')
def index():
    title = 'Добро пожаловать!'
    kinopoisk_id = current_app.config['DEFAULT_ID']
    if current_user.is_authenticated:
        films_list = Film.query.all()

        username = User.__repr__(current_user)
        film = Film.query.filter_by(kino_id=kinopoisk_id).first()
        return render_template('search/index.html', page_title=title, username=username, film=film, films_list=films_list)
    return render_template('search/index.html', page_title=title)


@blueprint.route('/video', methods=['POST', 'GET'])
def search():
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        if request.method == 'POST':
            result = request.form['search']
            result = result.lower().strip()
            print(result)
            id = get_response(result)
            if not Film.query.filter(Film.name == result).count():
                kino_scrap(id)
                film = Film.query.filter_by(kino_id=id).first()
                if not film:
                    film = id
                    print(f'id этого фильма {id}')
                    return render_template('search/index.html', page_title=result.capitalize(), result=result, username=username, film=film)
            film = Film.query.filter_by(kino_id=id).first()
            return render_template('search/index.html', page_title=result.capitalize(), result=result,
                                   username=username, film=film)
    return redirect(url_for('user.login'))
