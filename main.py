from flask import Flask
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads

from config import DB_FILE
from data import db_session
from routes import public_bp, admin_bp, route_utils


def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'srr61dSLjxW/BRSMmwoTcGDWiaCqcqGXp8BfdQ7Y+Uo='
    app.config['UPLOADED_FILES_DEST'] = 'static/uploads'
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    db_session.global_init(DB_FILE)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(route_utils.user_loader)
    login_manager.unauthorized_handler(route_utils.unauthorized)

    app.uploader = UploadSet()
    configure_uploads(app, app.uploader)

    app.run(port=8080)


if __name__ == '__main__':
    main()
