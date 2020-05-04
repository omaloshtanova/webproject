from wtforms import ValidationError


class Email(object):
    def __init__(self, message=None):
        if not message:
            message = 'Invalid email address.'
        self.message = message

    def __call__(self, form, field):
        if not ('@' in field.data or '.' in field.data):
            raise ValidationError(self.message)


class UniqueValue(object):
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field

        if not message:
            message = 'Value already exists.'
        self.message = message

    def __call__(self, form, field):
        if self.model.query().filter(self.field == field.data).first():
            raise ValidationError(self.message)
