from functools import wraps
from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect
from flask import Flask
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'srr61dSLjxW/BRSMmwoTcGDWiaCqcqGXp8BfdQ7Y+Uo='

from routes import *

AUTHORIZED_REDIRECT = '/'
UNAUTHORIZED_REDIRECT = '/login'
USER_ROLE = 1
ADMIN_ROLE = 2

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(UNAUTHORIZED_REDIRECT)


def for_anonymous(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            return redirect(AUTHORIZED_REDIRECT)
        return func(*args, **kwargs)
    return decorated


def for_admins(func):
    @wraps(func)
    def decorated1(*args, **kwargs):
        if current_user and current_user.is_role(ADMIN_ROLE):
            return func(*args, **kwargs)
        raise Forbidden()
    return decorated1


def main():
    db_session.global_init("db/db.sqlite")
    app.run(port=8080)


if __name__ == '__main__':
    main()
