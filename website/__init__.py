from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import json

db = SQLAlchemy()
DB_NAME = "track.db"

def create_app():
    # initialize flask
    app = Flask(__name__)
    # initialize token authentication and db
    app.config['SECRET_KEY'] = 'theverysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # relative import from package
    from .views import views
    from .catalog import catalog
    from .playlist import playlist

    # register blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(catalog, url_prefix='/')
    app.register_blueprint(playlist, url_prefix='/')

    from .models import Track, Score

    create_database(app)
    return app

def create_database(app):
    # check if db has been created, if yes just leave it
    # as we do not want to overwrite already existing datas
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

