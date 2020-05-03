from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo
from forms.validators import UniqueValue, Email
from data import User

DATA_REQUIRED_ERROR = 'Обязательное поле'
EMAIL_ERROR = 'Не верно указан email'
USER_UNIQUE_ERROR = 'Пользователь с таким email уже существует'
PASSWORD_LEN_ERROR = 'Пароль должен быть не менее %(min)d символов'
PASSWORD_AGAIN_ERROR = 'Пароль не совпадает'


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(message=DATA_REQUIRED_ERROR), Email(message=EMAIL_ERROR),
                                            UniqueValue(User, User.email, message=USER_UNIQUE_ERROR)])
    password = PasswordField('Пароль', validators=[DataRequired(message=DATA_REQUIRED_ERROR),
                                                   Length(6, message=PASSWORD_LEN_ERROR)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(message=DATA_REQUIRED_ERROR),
                                                                   EqualTo('password', message=PASSWORD_AGAIN_ERROR)])
    first_name = StringField('Имя', validators=[DataRequired(message=DATA_REQUIRED_ERROR)])
    last_name = StringField('Фамилия', validators=[DataRequired(message=DATA_REQUIRED_ERROR)])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(message=DATA_REQUIRED_ERROR), Email(message=EMAIL_ERROR)])
    password = PasswordField('Пароль', validators=[DataRequired(message=DATA_REQUIRED_ERROR),
                                                   Length(6, message=PASSWORD_LEN_ERROR)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
