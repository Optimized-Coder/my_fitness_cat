from flask import Flask, redirect, url_for

import os

from .extensions import db, migrate, login_manager
from .functions import get_daily_calories

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User

    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))
    
    # @login_manager.login_view
    # def login():
    #     return redirect(url_for('auth.login'))
    

    return app
