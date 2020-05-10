import os

from flask import Blueprint, current_app, render_template
from flask_login import current_user
from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect

from data import users, Animal, Breed, Exhibition
from forms.admin import *

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def _before():
    if current_user.is_authenticated and current_user.is_role(users.ADMIN_ROLE):
        return
    raise Forbidden()


@admin.route('/animals')
def animals_view():
    animals = Animal.query().order_by(Animal.name).all()
    return render_template('admin/animals_view.html', title='Животные', animals=animals)


@admin.route('/animals/new', methods=['GET', 'POST'])
def animal_create():
    form = AnimalForm()

    if form.validate_on_submit():
        Animal.create(**form.data)
        return redirect('/admin/animals')

    return render_template('admin/animal.html', title='Добавить животное', form=form)


@admin.route('/animals/<int:id>', methods=['GET', 'POST'])
def animal_update(id):
    animal = Animal.get_or_404(id)

    form = AnimalForm()

    if form.validate_on_submit():
        animal.update(**form.data)
        return redirect('/admin/animals')

    form.name.data = animal.name
    return render_template('admin/animal.html', title='Править животное', form=form)


@admin.route('/animals/<int:id>/delete')
def animal_delete(id):
    Animal.delete_by(Animal.id == id)
    return redirect('/admin/animals')


@admin.route('/breeds')
def breeds_view():
    breeds = Breed.query().order_by(Breed.name).all()
    return render_template('admin/breeds_view.html', title='Породы', breeds=breeds)


@admin.route('/breeds/new', methods=['GET', 'POST'])
def breed_create():
    animals = Animal.query().order_by(Animal.name).all()

    form = BreedForm()
    form.animal_id.choices = [(a.id, a.name) for a in animals]

    if form.validate_on_submit():
        filename = current_app.uploader.save(form.photo.data)
        form.photo.data = filename
        Breed.create(**form.data)
        return redirect('/admin/breeds')

    return render_template('admin/breed.html', title='Добавить породу', form=form)


@admin.route('/breeds/<int:id>', methods=['GET', 'POST'])
def breed_update(id):
    breed = Breed.get_or_404(id)
    animals = Animal.query().order_by(Animal.name).all()

    form = BreedForm()
    form.animal_id.choices = [(a.id, a.name) for a in animals]

    if form.validate_on_submit():
        filename = current_app.uploader.save(form.photo.data)
        form.photo.data = filename
        breed.update(**form.data)
        return redirect('/admin/breeds')

    form.animal_id.default = breed.animal_id
    form.process()
    form.name.data = breed.name
    form.photo.data = breed.photo
    form.about.data = breed.about
    return render_template('admin/breed.html', title='Править породу', form=form)


@admin.route('/breeds<int:id>/delete')
def breed_delete(id):
    breed = Breed.get_or_404(id)

    if breed.photo:
        file_path = current_app.uploader.path(breed.photo)
        if os.path.exists(file_path):
            os.remove(file_path)

    breed.delete()
    return redirect('/admin/breeds')


@admin.route('/exhibitions')
def exhibitions_view():
    exhibitions = Exhibition.query().order_by(Exhibition.date.desc()).all()
    return render_template('admin/exhibitions_view.html', title='Выставки', exhibitions=exhibitions)


@admin.route('/exhibitions/new', methods=['GET', 'POST'])
def exhibition_create():
    animals = Animal.query().order_by(Animal.name).all()

    form = ExhibitionForm()
    form.animal_id.choices = [(a.id, a.name) for a in animals]

    if form.validate_on_submit():
        Exhibition.create(**form.data)
        return redirect('/admin/exhibitions')

    return render_template('admin/exhibition.html', title='Добавить выставку', form=form)


@admin.route('/exhibitions/<int:id>', methods=['GET', 'POST'])
def exhibition_update(id):
    exhibition = Exhibition.get_or_404(id)
    animals = Animal.query().order_by(Animal.name).all()

    form = ExhibitionForm()
    form.animal_id.choices = [(a.id, a.name) for a in animals]

    if form.validate_on_submit():
        exhibition.update(**form.data)
        return redirect('/admin/exhibitions')

    form.animal_id.default = exhibition.animal_id
    form.process()
    form.name.data = exhibition.name
    form.date.data = exhibition.date
    form.address.data = exhibition.address
    form.about.data = exhibition.about
    return render_template('admin/exhibition.html', title='Править выставку', form=form)


@admin.route('/exhibitions/<int:id>/delete')
def exhibition_delete(id):
    Exhibition.delete_by(Exhibition.id == id)
    return redirect('/admin/exhibitions')

