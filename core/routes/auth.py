from flask import Blueprint, redirect, url_for, request, flash, render_template
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
    
'''
Login routes
'''

@auth.route('/login/', methods=['GET'])
def login_get():
    if not current_user.is_authenticated:
        context = {
            'title': 'Login | My Fitness Cat',
        }
        return render_template(
            'auth/login.html',
            **context
        )
    else:
        return redirect(url_for('main.index'))

@auth.route('/login/', methods=['POST'])
def login():
    if not current_user.is_authenticated:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=True)
            flash('Logged in', 'success')
            return redirect(url_for('main.get_cats'))
    else: 
        flash('Already Logged in')
        return redirect(url_for('main.get_cats'))

'''
register routes
'''

@auth.route('/register/', methods=['GET'])
def register_get():
    if not current_user.is_authenticated:
        context = {
            'title': 'Register | My Fitness Cat'
        }

        return render_template(
            'auth/register.html',
            **context
        )
    else:
        return redirect(url_for('main.index'))
    
@auth.route('/register/', methods=['POST'])
def register():
    if not current_user.is_authenticated:
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        email = request.form.get('email')
        first_name = request.form.get('f_name')

        # validation
        if not validate_password(password):
            flash('Invalid password.')
            return redirect(url_for('auth.register'))
        elif not password == password_check:
            flash('Passwords do not')
            return redirect(url_for('auth.register'))
        elif not validate_email(email):
            flash('Invalid email.')
            return redirect(url_for('auth.register'))
        elif not validate_username(username):
            flash('Invalid username.')
            return redirect(url_for('auth.register'))
        else: 
            password_hash = generate_password_hash(password, method='sha256')

        # create new user
        user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            first_name=first_name,
        )

        db.session.add(user)
        db.session.commit()

        return 'User added'
    else:
        return 'Already Logged in'

'''
Logout routes
'''
    
@auth.route('/logout/')
def logout():
    if not current_user.is_authenticated:
        flash("You are not logged in", "error")
        return redirect(url_for('auth.login'))
    else:
        logout_user()
        flash("Logged Out Successfully", "success")
        return redirect(url_for('auth.login'))