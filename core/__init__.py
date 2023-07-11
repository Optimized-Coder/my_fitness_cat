from flask import Flask, redirect, url_for

import os

from .extensions import db, migrate, login_manager
from .functions import get_daily_calories, validate_password

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FLASK_APP='core',
        FLASK_DEBUG=True,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User, owner_cat, Cat, Food, cat_food

    from .routes import main, auth, food
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(food)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    
    @app.route('/test/')
    def test():
        password = validate_password('Hello123')

        if password:
            return 'true'
        else:
            return 'false'

    return app
