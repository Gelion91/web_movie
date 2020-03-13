from flask import Blueprint, render_template, request
from flask_login import current_user

from web_movie import get_response, User

blueprint = Blueprint('search', __name__)


@blueprint.route('/')
def index():
    title = 'Добро пожаловать!'
    if current_user.is_authenticated:
        username = User.__repr__(current_user)
        return render_template('search/index.html', page_title=title, username=username)
    return render_template('search/index.html', page_title=title)


@blueprint.route('/video', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        result = request.form['search']
        kinopoisk_id = get_response(result)
        return render_template('search/index.html', page_title=result, kinopoisk_id=kinopoisk_id, result=result)
