from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fee project semester1'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.abspath("website/" + DB_NAME)}'
    db.init_app(app)

    # app.config['LOGIN_MESSAGE'] = "You must be logged in to access Home page!"
    # app.config['LOGIN_MESSAGE_CATEGORY'] = "error"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # views = Blueprint('views', __name__)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) 

    # --------------------------------------Email code-------------------------------------
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'kabirjeet0370.becse24@chitkara.edu.in'
    app.config['MAIL_PASSWORD'] = 'pubx rirl wsrp mtid'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')