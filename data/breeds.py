import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .mixins import CRUDMixin


class Breed(SqlAlchemyBase, CRUDMixin):
    __tablename__ = 'breeds'

    name = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    animal_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("animals.id"))
    animal = orm.relation('Animal')
