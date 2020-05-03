from functools import wraps
from flask_login import current_user
from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect

from config import UNAUTHORIZED_REDIRECT, AUTHORIZED_REDIRECT
from data import db_session, users, User


def user_loader(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def unauthorized():
    return redirect(UNAUTHORIZED_REDIRECT)


def for_anonymous(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print(current_user)
        if current_user.is_anonymous:
            return func(*args, **kwargs)
        return redirect(AUTHORIZED_REDIRECT)
    return decorated


def for_admins(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_role(users.ADMIN_ROLE):
            return func(*args, **kwargs)
        raise Forbidden()
    return decorated
