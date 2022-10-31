from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ndkbmrwojtuytf:e60ef8a95fbc1e54d3f8aed0ebd2e9769b5a6b59197448ab85d6b0f81d9ef64b@ec2-44-199-22-207.compute-1.amazonaws.com:5432/d2a6uhbrjrvj9q'

    #db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    #create_database(app)
    db.create_all()
    
    loging_manager = LoginManager()
    loging_manager.login_view = 'auth.login'
    loging_manager.init_app(app)

    @loging_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        #db.create_all(app=app)
        db.create_all()
        print('Created Database!')