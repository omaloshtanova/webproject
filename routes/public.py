from flask import Blueprint
from data import db_session, users, User
from flask import render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect
from forms.public import *
from .utils import for_anonymous

public = Blueprint('public', __name__, template_folder='public')


@public.route('/')
def index():
    return render_template('main.html', title='Главная')


@public.route('/about')
def about():
    return render_template('about.html', title='О нас')


@public.route('/register', methods=['GET', 'POST'])
@for_anonymous
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = db_session.create_session()

        user = User()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.about = form.about.data
        user.set_password(form.password.data)
        user.role_id = users.USER_ROLE
        session.add(user)
        session.commit()

        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@public.route('/login', methods=['GET', 'POST'])
@for_anonymous
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html', title='Авторизация', message="Неправильный логин или пароль", form=form)

    return render_template('login.html', title='Авторизация', form=form)


@public.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect("/")
