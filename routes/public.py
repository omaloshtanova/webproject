from flask import Blueprint, current_app
from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
from werkzeug.utils import redirect

from data import *
from forms.public import *
from .utils import for_anonymous

public = Blueprint('public', __name__)


@public.route('/')
def index():
    random_breed = Breed.query().order_by(func.random()).first()
    last_exhibitions = Exhibition.query().order_by(Exhibition.date.desc()).limit(3).all()
    return render_template('main.html', title='Главная', app=current_app, breed=random_breed, exhibitions=last_exhibitions)


@public.route('/about')
def about():
    return render_template('about.html', title='О нас')


@public.route('/animals/<int:id>')
def breeds(id):
    animal = Animal.get_or_404(id)
    all_breeds = Breed.filter(Breed.animal_id == id).order_by(Breed.name).all()
    return render_template('breeds.html', current_app=current_app, title=animal.name, breeds=all_breeds)


@public.route('/exhibitions')
def exhibitions():
    all_exhibitions = Exhibition.query().order_by(Exhibition.date.desc()).all()
    return render_template('exhibitions.html', title='Выставки', exhibitions=all_exhibitions)


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


@public.route('/exs')
@login_required
def exs():
    my_exhibitions = Exhibition.query().join(Exhibition.pets).filter(Pet.user_id == current_user.id).all()
    return render_template('my_exhibitions.html', title='Мои Выставки', exhibitions=my_exhibitions)


@public.route('/order/<int:id>', methods=['GET', 'POST'])
@login_required
def order(id):
    exhibition = Exhibition.get_or_404(id)
    my_pets = Pet.query().order_by(Pet.name).all()

    form = OrderForm()
    form.pet_id.choices = [(a.id, a.name) for a in my_pets]

    if form.validate_on_submit():
        session = exhibition._db_session()
        pet = session.merge(Pet.get(form.pet_id.data))
        exhibition.pets.append(pet)
        session.add(exhibition)
        session.commit()
        return redirect('/exs')

    return render_template('order.html', title='Записаться на выставку', form=form, exhibition=exhibition)
