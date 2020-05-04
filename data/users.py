import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from .mixins import CRUDMixin

USER_ROLE = 1
ADMIN_ROLE = 2


class User(SqlAlchemyBase, UserMixin, CRUDMixin):
    __tablename__ = 'users'

    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    role_id = sqlalchemy.Column(sqlalchemy.Integer)

    fillable = ['first_name', 'last_name', 'email']

    @classmethod
    def create(cls, commit=True, **kwargs):
        fillable = cls._get_fillable(kwargs)
        user = cls(**fillable)
        user.set_password(kwargs['password'])
        user.role_id = USER_ROLE
        return user.save(commit=commit)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_role(self, role_id):
        return self.role_id == role_id
