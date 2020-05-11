from flask import Blueprint, current_app
from data import users, User, Animal, Breed, Exhibition
from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from data.pets import Pet
from forms.public import *
from .utils import for_anonymous

public = Blueprint('public', __name__)


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
        User.create(**form.data)
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@public.route('/login', methods=['GET', 'POST'])
@for_anonymous
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query().filter(User.email == form.email.data).first()

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


@public.route('/animals')
def animals():
    all_animals = Animal.query().order_by(Animal.name).all()
    return render_template('animals.html', title='Животные', animals=all_animals)


@public.route('/animals/<int:id>')
def breeds(id):
    animal = Animal.get_or_404(id)
    all_breeds = Breed.filter(Breed.animal_id == id).order_by(Breed.name).all()
    return render_template('breeds.html', current_app=current_app, title=animal.name, breeds=all_breeds)


@public.route('/exhibitions')
def exhibitions():
    all_exhibitions = Exhibition.query().order_by(Exhibition.date.desc()).all()
    return render_template('exhibitions.html', title='Выставки', exhibitions=all_exhibitions)


@public.route('/pets')
@login_required
def pets():
    my_pets = Pet.filter(current_user.id == Pet.user_id).order_by(Pet.name).all()
    return render_template('my_pets.html', title='Мои животные', pets=my_pets)


@public.route('/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    breeds = Breed.query().order_by(Breed.name).all()

    form = AddPetForm()
    form.breed_id.choices = [(a.id, a.name) for a in breeds]
    form.user_id.data = current_user.id

    if form.validate_on_submit():
        Pet.create(**form.data)
        return redirect('/pets')

    return render_template('add_pet.html', title='Добавить питомца', form=form)
