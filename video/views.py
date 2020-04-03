from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user
from web_movie import get_response, User
from .models import Film
blueprint = Blueprint('search', __name__)


@blueprint.route('/')
@blueprint.route('/<int:page>', methods=['POST', 'GET'])
def index(page=1):
    title = 'Добро пожаловать!'
    films_list = Film.query.paginate(page, current_app.config['FILM_PER_PAGE'], False)
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        return render_template('start.html', page_title=title, username=username, films_list=films_list)
    return render_template('start.html', page_title=title, films_list=films_list)


@blueprint.route('/video', methods=['POST', 'GET'])
def search():
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        if request.method == 'POST':
            result = request.form['search']
            result = result.lower().strip()
            print(result)
            id = get_response(result)
            film = Film.query.filter_by(kino_id=id).first()
            if not film:
                film = id
                print(f'id этого фильма {id}')
                return render_template('search/index.html', page_title=result.capitalize(), result=result, username=username, film=film)
            print('беру из базы')
            return render_template('search/index.html', page_title=result.capitalize(), result=result,
                                   username=username, film=film)
    return redirect(url_for('user.login'))
