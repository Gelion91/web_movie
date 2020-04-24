from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user
from .models import Film
from web_movie.user.models import User

blueprint = Blueprint('search', __name__)


@blueprint.route('/')
@blueprint.route('/page/<int:page>', methods=['POST', 'GET'])
def index(page=1):
    title = 'Добро пожаловать!'
    films_list = Film.query.paginate(page, current_app.config['FILM_PER_PAGE'], False)
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        return render_template('start.html', page_title=title, username=username, films_list=films_list)
    return render_template('start.html', page_title=title, films_list=films_list)


@blueprint.route('/category/<name>')
@blueprint.route('/category/<name>/<int:page>')
def category(name, page=1):
    title = name
    films_list = Film.query.filter(Film.category.like('%{}%'.format(name))).paginate(page, current_app.config['FILM_PER_PAGE'], False)
    print(films_list.items)
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        return render_template('films/category.html', page_title=title, username=username, films_list=films_list, name=name)
    return render_template('start.html', page_title=title, films_list=films_list, name=name)


@blueprint.route('/search', methods=['POST', 'GET'])
@blueprint.route('/search/<int:page>', methods=['POST', 'GET'])
def search(page=1):
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        if request.method == 'POST':
            result = request.form['search']
            result = result.lower().strip()
            title = result
            films_list = Film.query.filter(Film.name.like('%{}%'.format(result))).paginate(page, current_app.config['FILM_PER_PAGE'], False)
            print(films_list.items)
            return render_template('start.html', page_title='запрос: ' + title, username=username, films_list=films_list)
    return redirect(url_for('user.login'))
