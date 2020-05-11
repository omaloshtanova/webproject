import sqlalchemy
from .db_session import SqlAlchemyBase


class ExhibitionPet(SqlAlchemyBase):
    __tablename__ = 'exhibition_pet'

    exhibition_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exhibitions.id"), primary_key=True)
    pet_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("pets.id"), primary_key=True)
