from functools import wraps
from flask import Flask
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

from routes import *

AUTHORIZED_REDIRECT = '/'
UNAUTHORIZED_REDIRECT = '/login'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(UNAUTHORIZED_REDIRECT)


def anonymous_only(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            return redirect(AUTHORIZED_REDIRECT)
        return func(*args, **kwargs)
    return decorated


# def anonymous_only(url='/'):
#     def decorator(func):
#         @wraps(func)
#         def decorated_view(*args, **kwargs):
#             if current_user and current_user.is_authenticated:
#                 return redirect(url)
#             return func(*args, **kwargs)
#         return decorated_view
#     return decorator


def main():
    db_session.global_init("db/db.sqlite")
    app.run(port=8080)


if __name__ == '__main__':
    main()
