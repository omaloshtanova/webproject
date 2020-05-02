from data import db_session
from main import app, anonymous_only
from flask import render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect
from forms.forms import *


@app.route('/')
def index():
    return render_template('main.html', title='Главная')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/register', methods=['GET', 'POST'])
@anonymous_only
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = db_session.create_session()

        user = User(
            first_name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html', message="Неправильный логин или пароль", form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
