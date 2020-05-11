import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .mixins import CRUDMixin


class Animal(SqlAlchemyBase):
    __tablename__ = 'exhibition_pet'

    exhibition_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exhibitions.id"))
    pet_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("pets.id"))

    # sqlalchemy.Column('news', sqlalchemy.Integer, sqlalchemy.ForeignKey('news.id')),

