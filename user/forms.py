from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    remember_me = BooleanField('Запомнить', default=True, render_kw={'class': 'form-check-input'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class RegForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password_reply = PasswordField('Повторите пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})