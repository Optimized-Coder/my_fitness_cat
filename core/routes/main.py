from flask import Blueprint, request
from flask_login import current_user, login_required

from ..models import Cat, owner_cat
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



@main.route('/my-cats/', methods=['GET'])
@login_required
def get_user_cats():
    user = current_user
    cats = user.cats

    if cats.count() > 0:
        return [cat.to_dict() for cat in cats]
    else:
        return 'No cats found'
    
@main.route('/my-cats/<int:cat_id>/', methods=['GET'])
@login_required
def get_cat(cat_id):
    user=current_user
    cats = user.cats

    return [cat.to_dict() for cat in cats if cat.id == cat_id]

@main.route('/my-cats/<int:cat_id>/delete/', methods=['DELETE'])
@login_required
def delete_cat(cat_id):
    user=current_user
    cats = user.cats
    cat = Cat.query.get(cat_id)

    if cat:
        db.session.delete(cat)
        db.session.commit()
        return f'cat: {cat.name} deleted'
    
    return 'Cat not found'

@main.route('/my-cats/<int:cat_id>/edit/', methods=['POST'])
@login_required
def edit_cat(cat_id):
    user=current_user
    cats = user.cats
    cat = Cat.query.get(cat_id)

    weight = request.form.get('weight')
    weight_class = request.form.get('weight_class')
    is_neutered_input = request.form.get('is_neutered')
    age = request.form.get('age')
    breed = request.form.get('breed')
    color = request.form.get('color')

    if cat:
        cat.weight = int(weight)
        cat.weight_class = str(weight_class)
        cat.is_neutered = True if is_neutered_input == 'true' else False
        cat.age = int(age)
        cat.breed = str(breed).strip()
        cat.color = str(color).strip()
        db.session.commit()
        return f'cat: {cat.name} edited'
    
    return 'Cat not found'

