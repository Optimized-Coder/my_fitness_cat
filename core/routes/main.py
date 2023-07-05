from flask import Blueprint, request
from flask_login import current_user, login_required

from ..models import User, Cat, owner_cat
from ..extensions import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return '<h1>Main route</h1>'

@main.route('/add-cat/', methods=['POST'])
@login_required
def add_cat():
    user = current_user
    weight = request.form.get('weight')
    weight_class = request.form.get('weight_class')
    is_neutered_input = request.form.get('is_neutered')
    name = request.form.get('name')

    if is_neutered_input == 'false':
        is_neutered = False
    elif is_neutered_input == 'true':
        is_neutered = True
    else:
        return 'Please enter a valid input'

    new_cat = Cat(
        weight=int(weight),
        weight_class=weight_class,
        is_neutered=is_neutered,
        name=name
    )

    db.session.add(new_cat)
    db.session.commit()

    user_cat = owner_cat.insert().values(
        owner_id=user.id,
        cat_id=new_cat.id
    )

    db.session.execute(user_cat)
    db.session.commit()

    return 'Cat added'



@main.route('/my-cats/')
@login_required
def get_user_cats():
    user = current_user
    cats = user.cats

    if cats.count() > 0:
        return [cat.to_dict() for cat in cats]
    else:
        return 'No cats found'