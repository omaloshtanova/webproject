from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect

from data import users, Animal
from forms.admin import *


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def _before():
    if current_user.is_authenticated and current_user.is_role(users.ADMIN_ROLE):
        return
    raise Forbidden()


@admin.route('/animals')
def animal_view():
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

