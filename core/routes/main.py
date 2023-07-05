from flask import Blueprint, request, render_template
from flask_login import current_user, login_required

from datetime import date

from ..models import Cat, owner_cat
from ..extensions import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    context = {
        'title': 'Home | My Fitness Cat'
    }

    return render_template(
        'main/index.html',
        **context
    )

@main.route('/add-cat/', methods=['POST'])
@login_required
def add_cat():
    user = current_user
    weight = request.form.get('weight')
    weight_class = request.form.get('weight_class')
    is_neutered_input = request.form.get('is_neutered')
    name = request.form.get('name')
    dob_day = request.form.get('dob_day')
    dob_month = request.form.get('dob_month')
    dob_year = request.form.get('dob_year')

    dob = date(day=int(dob_day), month=int(dob_month), year=int(dob_year))

    if is_neutered_input == 'false':
        is_neutered = False
    elif is_neutered_input == 'true':
        is_neutered = True
    else:
        return 'Please enter a valid input'

    new_cat = Cat(
        weight=float(weight),
        weight_class=weight_class,
        is_neutered=is_neutered,
        name=name,
        dob=dob
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
    dob_day = request.form.get('dob_day')
    dob_month = request.form.get('dob_month')
    dob_year = request.form.get('dob_year')

    breed = request.form.get('breed')
    color = request.form.get('color')

    if cat:
        if weight:
            cat.weight = float(weight)
        if weight_class:
            cat.weight_class = str(weight_class)
        if is_neutered_input:
            cat.is_neutered = True if is_neutered_input == 'true' else False
        if dob_day and dob_month and dob_year:
            cat.dob = date(day=int(dob_day), month=int(dob_month), year=int(dob_year))
        if breed:
            cat.breed = str(breed).strip()
        if color:
            cat.color = str(color).strip()

        db.session.commit()
        return f'cat: {cat.name} edited'
    
    raise ValueError('Cat not found')


