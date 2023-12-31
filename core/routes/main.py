from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required

from datetime import date

from ..models import Cat, owner_cat, Food, cat_food
from ..extensions import db
from ..functions import get_user_cats

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    name = request.args.get('name')
    weight = request.args.get('weight')
    age = request.args.get('age')

    if weight and name and age:
        calories = round(int(weight) ** 0.75 * 70 * 1.6)
    else:
        calories = 0

    context = {
        'title': 'Home | My Fitness Cat',
        'name': name,
        'weight': weight,
        'age': age,
        'calories': calories
    }

    return render_template(
        'main/index.html',
        **context
    )

'''
Add cat routes
'''

@main.route('/add-cat/', methods=['GET'])
@login_required
def add_cat_get():
    context = {
        'title': 'Add Cat | My Fitness Cat'
    }
    return render_template(
        'main/add.html',
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

    dob = date(
        day=int(dob_day), 
        month=int(dob_month), 
        year=int(dob_year)
    )

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

    return redirect(url_for('main.get_cats'))

'''
View cats routes
'''

@main.route('/my-cats/', methods=['GET'])
@login_required
def get_cats():
    cats = [cat for cat in current_user.cats]
    print(cats)

    context = {
        'title': 'My Cats | My Fitness Cat',
        'cats': cats,
        'user': current_user
    }
    return render_template(
        'main/view_all.html',
        **context
    )

@main.route('/my-cats/json/', methods=['GET'])
@login_required
def get_cats_json():
    cats = [cat.to_dict() for cat in get_user_cats()]

    return jsonify(cats)

    
@main.route('/my-cats/<int:cat_id>/', methods=['GET'])
@login_required
def get_cat(cat_id):
    found_cat = [cat.to_dict() for cat in get_user_cats() if cat.id == cat_id]

    context = {
        'title': 'My Cats | My Fitness Cat',
        'found_cat': found_cat[0]
    }
    return render_template(
        'main/view_one.html',
        **context
    )

@main.route('/my-cats/<int:cat_id>/json/', methods=['GET'])
@login_required
def get_cat_json(cat_id):
    found_cat = [cat.to_dict() for cat in get_user_cats() if cat.id == cat_id]

    return jsonify(found_cat)

# @main.route('/my-cats/<int:cat_id>/delete/', methods=['DELETE'])
# @login_required
# def delete_cat_get(cat_id):


@main.route('/my-cats/<int:cat_id>/delete/', methods=['GET'])
@login_required
def delete_cat(cat_id):
    cats = [cat for cat in get_user_cats() if cat.id == cat_id]
    found_cat = cats[0]
    if found_cat:
        db.session.delete(found_cat)
        db.session.commit()
        flash(f'Cat {found_cat.name} deleted')
        return redirect(url_for('main.get_cats'))
    
    raise ValueError('Cat not found')

'''
edit cat routes
'''

@main.route('/my-cats/<int:cat_id>/edit/', methods=['GET'])
@login_required
def edit_cat_get(cat_id):
    cats = [cat for cat in get_user_cats() if cat.id == cat_id]
    found_cat = cats[0]

    context = {
        'title': 'Edit Cat | My Fitness Cat',
        'found_cat': found_cat
    }

    return render_template(
        'main/edit-cat.html',
        **context
    )

@main.route('/my-cats/<int:cat_id>/edit/', methods=['POST'])
@login_required
def edit_cat(cat_id):
    found_cat = [cat for cat in get_user_cats() if cat.id == cat_id][0]

    weight = request.form.get('weight')
    weight_class = request.form.get('weight_class')
    is_neutered_input = request.form.get('is_neutered')
    dob_day = request.form.get('dob_day')
    dob_month = request.form.get('dob_month')
    dob_year = request.form.get('dob_year')

    breed = request.form.get('breed')
    color = request.form.get('color')

    if found_cat:
        if weight:
            found_cat.weight = float(weight)
        if weight_class:
            found_cat.weight_class = str(weight_class)
        if is_neutered_input:
            found_cat.is_neutered = True if is_neutered_input == 'true' else False
        if dob_day and dob_month and dob_year:
            found_cat.dob = date(day=int(dob_day), month=int(dob_month), year=int(dob_year))
        if breed:
            found_cat.breed = str(breed).strip()
        if color:
            found_cat.color = str(color).strip()

        db.session.commit()
        return redirect(url_for('main.get_cats'))
    
    raise ValueError('Cat not found')

@main.route('/my-cats/<int:cat_id>/add-food/<int:food_id>/')
@login_required
def add_cat_food(cat_id, food_id):
    cat = Cat.query.get(cat_id)
    food = Food.query.get(food_id)

    if cat is None or food is None:
        return 'Invalid cat or food ID'

    existing_food = db.session.query(cat_food).filter(cat_food.c.cat_id == cat_id).first()

    if existing_food:
        delete_query = cat_food.delete().where(cat_food.c.cat_id == cat_id)
        db.session.execute(delete_query)
        db.session.commit()

    insert_query = cat_food.insert().values(cat_id=cat_id, food_id=food_id)
    db.session.execute(insert_query)
    db.session.commit()

    return 'Cat food added successfully'