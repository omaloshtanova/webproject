from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

DATA_REQUIRED_ERROR = 'Обязательное поле'


class AnimalForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message=DATA_REQUIRED_ERROR)])
    submit = SubmitField('Сохранить')
