import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .mixins import CRUDMixin


class Exhibition(SqlAlchemyBase, CRUDMixin):
    __tablename__ = 'exhibitions'

    name = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    animal_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("animals.id"))
    animal = orm.relation('Animal')
