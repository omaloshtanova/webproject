import datetime
import sqlalchemy
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .db_session import db_session


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    fillable = None

    @classmethod
    def create(cls, commit=True, **kwargs):
        fillable = cls._get_fillable(kwargs)
        instance = cls(**fillable)
        return instance.save(commit=commit)

    @classmethod
    def query(cls):
        return cls._db_session().query(cls)

    @classmethod
    def get(cls, id):
        return cls.query().get(id)

    @classmethod
    def get_or_404(cls, id):
        return cls.query().get_or_404(id)

    @classmethod
    def all(cls):
        return cls.query().all()

    @classmethod
    def filter(cls, criterion):
        return cls.query().filter(criterion)

    def update(self, commit=True, **kwargs):
        fillable = type(self)._get_fillable(**kwargs)
        for attr, value in fillable.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        self._db_session().add(self)
        print(self._db_session())
        if commit:
            self._db_session().commit()
        return self

    def delete(self, commit=True):
        self._db_session().delete(self)
        return commit and self.db_session.commit()

    @classmethod
    def _db_session(cls):
        if not hasattr(cls, 'db_session'):
            cls.db_session = db_session()
        return cls.db_session

    @classmethod
    def _get_fillable(cls, attrs):
        attrs = attrs.copy()
        for name in list(attrs):
            if cls.fillable:
                if name not in cls.fillable:
                    del attrs[name]
            else:
                if not hasattr(cls, name):
                    del attrs[name]
                else:
                    attr = getattr(cls, name)
                    if not isinstance(attr, InstrumentedAttribute):
                        del attrs[name]
        return attrs
