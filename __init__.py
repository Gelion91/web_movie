from flask import Flask, render_template, request
from web_movie.ya_api import get_response
from web_movie.model import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        id = app.config['DEFAULT_ID']
        return render_template('index.html', id=id)

    @app.route('/search', methods=['POST', 'GET'])
    def search():
        if request.method == 'POST':
            result = request.form['search']
            result = result.split('=')
            kinopoisk_id = get_response(result)
            id = result[-1]
            return render_template('index.html', id=id, kinopoisk_id=kinopoisk_id)
    return app
