from flask import Blueprint, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import User
from ..extensions import db
from ..functions import validate_password, validate_email, validate_username

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.index'))
    

@auth.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        flash('Invalid username or password')
        return redirect(url_for('auth.login'))
    else:
        login_user(user, remember=True)
        return redirect(url_for('main.index'))

    
@auth.route('/register/', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    first_name = request.form.get('f_name')
    last_name = request.form.get('l_name')

    # validation
    if not validate_password(password):
        flash('Invalid password.')
        return redirect(url_for('auth.register'))
    elif not validate_email(email):
        flash('Invalid email.')
        return redirect(url_for('auth.register'))
    elif not validate_username(username):
        flash('Invalid username.')
        return redirect(url_for('auth.register'))     
    else: 
        password_hash = generate_password_hash(password, method='sha256')

    user = User(
        username=username,
        password_hash=password_hash,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    db.session.add(user)
    db.session.commit()

    return 'User added'

    
@auth.route('/logout/')
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        logout_user()
        return redirect(url_for('auth.login'))