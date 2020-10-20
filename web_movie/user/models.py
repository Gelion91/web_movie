from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from web_movie import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '{}'.format(self.username)


class MovieModelView(ModelView):
    excluded_list_columns = ('content', 'music_author', 'writers', 'operator', 'rating', 'tags', 'actors')

    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return abort(404)
        else:
            return current_user.is_authenticated
