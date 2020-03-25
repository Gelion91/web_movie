from web_movie.parse.ya_api import get_response
from web_movie.video.db import db
from flask import Flask
from flask_login import LoginManager
from web_movie.user.models import User
from web_movie.user.views import blueprint as user_blueprint
from web_movie.admin.views import blueprint as admin_blueprint
from web_movie.video.views import blueprint as video_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(video_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
