import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .mixins import CRUDMixin


class Animal(SqlAlchemyBase, CRUDMixin):
    __tablename__ = 'animals'

    name = sqlalchemy.Column(sqlalchemy.String)
    breeds = orm.relation("Breed", backref="animals")
