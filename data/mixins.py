import datetime
import sqlalchemy
from .db_session import db_session

fillable = None


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    fillable = None

    @classmethod
    def create(cls, commit=True, **kwargs):
        fillable = cls._get_fillable(**kwargs)
        instance = cls(**fillable)
        return instance.save(commit=commit)

    @classmethod
    def query(cls):
        return db_session().query(cls)

    @classmethod
    def get(cls, id):
        return cls.query().get(id)

    @classmethod
    def get_or_404(cls, id):
        return cls.query().get_or_404(id)

    def update(self, commit=True, **kwargs):
        fillable = type(self)._get_fillable(kwargs)
        for attr, value in fillable.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db_session().add(self)
        if commit:
            db_session().commit()
        return self

    def delete(self, commit=True):
        db_session().delete(self)
        return commit and db_session().commit()

    @classmethod
    def _get_fillable(cls, **kwargs):
        for attr in list(kwargs):
            if fillable:
                if attr not in fillable:
                    del kwargs[attr]
            else:
                if not hasattr(cls, attr) or not isinstance(attr, sqlalchemy.Column):
                    del kwargs[attr]
        return kwargs
