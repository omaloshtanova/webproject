from wtforms import ValidationError
from data import db_session


class Email(object):
    def __init__(self, message=None):
        if not message:
            message = 'Invalid email address.'
        self.message = message

    def __call__(self, form, field):
        if not ('@' in field.data or '.' in field.data):
            raise ValidationError(self.message)


class UniqueValue(object):
    def __init__(self, table, table_field, message=None):
        self.table = table
        self.table_field = table_field

        if not message:
            message = 'Invalid email address.'
        self.message = message

    def __call__(self, form, field):
        session = db_session.create_session()
        if session.query(self.table).filter(self.table_field == field.data).first():
            raise ValidationError(self.message)
