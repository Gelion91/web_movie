from flask_login import login_user, logout_user, current_user
from flask import render_template, flash, redirect, url_for, Blueprint

from db import db
from web_movie.user.forms import LoginForm, RegForm
from web_movie.user.models import User

blueprint = Blueprint('user', __name__)


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.logout'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно авторизованы')
            return redirect(url_for('search.index'))
    flash('Неправильное имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли из аккаунта')
    return redirect(url_for('search.index'))


@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('search.index'))
    title = 'Регистрация'
    reg_form = RegForm()
    return render_template('user/registration.html', page_title=title, form=reg_form)


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    form = RegForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('search.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text,
                                                        error
                                                        ))
        return redirect(url_for('user.registration'))
