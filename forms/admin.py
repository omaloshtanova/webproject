from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_uploads import IMAGES
from wtforms import StringField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired

DATA_REQUIRED_ERROR = 'Обязательное поле'
IMAGES_ERROR = 'Только изображения'


class AnimalForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message=DATA_REQUIRED_ERROR)])
    submit = SubmitField('Сохранить')


class BreedForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message=DATA_REQUIRED_ERROR)])
    animal_id = SelectField('Тип животного', validate_choice=False)
    photo = FileField('Фото животного', validators=[FileAllowed(IMAGES, message=IMAGES_ERROR)])
    about = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
