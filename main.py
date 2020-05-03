from flask import Flask
from flask_login import LoginManager
from data import db_session
from routes import public_routes, admin_routes, route_utils


def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'srr61dSLjxW/BRSMmwoTcGDWiaCqcqGXp8BfdQ7Y+Uo='
    app.register_blueprint(public_routes)
    app.register_blueprint(admin_routes)

    db_session.global_init("db/db.sqlite")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(route_utils.user_loader)
    login_manager.unauthorized_handler(route_utils.unauthorized)

    app.run(port=8080)


if __name__ == '__main__':
    main()
