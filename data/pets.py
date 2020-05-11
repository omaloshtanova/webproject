import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .mixins import CRUDMixin


class Pet(SqlAlchemyBase, CRUDMixin):
    __tablename__ = 'pets'

    name = sqlalchemy.Column(sqlalchemy.String)
    number = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    breed_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("breeds.id"))
    user = orm.relation("User")
    breed = orm.relation("Breed")
