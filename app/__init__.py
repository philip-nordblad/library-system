from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import secrets



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #Set up with imports
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Import and register models here
    from . import models

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Import and register your blueprints here
    from . import auth
    app.register_blueprint(auth.bp)
    # app.register_blueprint(main.bp)
    @app.route('/')
    def index():
        return render_template('index.html')

    return app