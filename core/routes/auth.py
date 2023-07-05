from flask import Blueprint, redirect, url_for
from flask_login import current_user

auth = Blueprint('auth', __name__, url_prefix='/auth')

# @auth.route('/')
# def index():
#     if not current_user.is_authenticated:
#         return redirect(url_for('auth.login'))
#     else:
#         return redirect(url_for('main.index'))

# @auth.route('/login')
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     else:
#         return '<h1>Login Page</h1>'
    
# @auth.route('/register/')
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     else:
#         return '<h1>Register Page</h1>'
    
# @auth.route('/logout/')
# def logout():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     else:
#         return '<h1>Logout Page</h1>'