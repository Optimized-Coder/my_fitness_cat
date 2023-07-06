from flask import Blueprint, request, render_template, jsonify

from ..extensions import db
from ..models import Food

food = Blueprint('food', __name__, url_prefix='/food')

'''
Add food routes
'''

@food.route('/add/', methods=['GET'])
def add_food_get():

    context = {
        'title': 'Add Food',
    }

    return render_template(
        'food/add.html',
        **context
    )

@food.route('/add/', methods=['POST'])
def add_food():
    flavour = request.form.get('flavour')
    wet_or_dry = request.form.get('wet_or_dry')
    age = request.form.get('age')
    calories = request.form.get('calories')
    packaging = request.form.get('packaging')
    weight_g = request.form.get('weight_g')

    food = Food(
        flavour=flavour,
        wet_or_dry=wet_or_dry,
        age=age,
        calories=int(calories),
        packaging=packaging,
        weight_g=int(weight_g)
    )

    db.session.add(food)
    db.session.commit()

    return f'Food: {food.flavour} added'

'''
View food routes
'''

@food.route('/view/json/', methods=['GET'])
def view_food_json():
    foods = [food.to_dict() for food in Food.query.all()]

    return jsonify(foods)

@food.route('/view/', methods=['GET'])
def view_food():
    foods = Food.query.all()

    context = {
        'title': 'View Food',
        'foods': foods
    }

    return render_template(
        'food/view-all.html',
        **context
    )

@food.route('/view/json/<int:food_id>/', methods=['GET'])
def view_food_one_json(food_id):
    one_food = Food.query.get(food_id)

    return jsonify(one_food.to_dict())

@food.route('/view/<int:food_id>/')
def view_one_food(food_id):
    one_food = Food.query.get(food_id)

    context = {
        'title': 'View Food',
        'food': one_food
    }
    return render_template(
        'food/view-one.html',
        **context
    )



'''
Edit food routes
'''

@food.route('/edit/<int:food_id>/', methods=['GET'])
def edit_food_get(food_id):
    one_food = Food.query.get(food_id)

    context = {
        'title': 'Edit Food',
        'food': one_food
    }

    return render_template(
        'food/edit.html',
        **context
    )

@food.route('/edit/<int:food_id>/', methods=['POST'])
def edit_food(food_id):
    flavour = request.form.get('flavour')
    wet_or_dry = request.form.get('wet_or_dry')
    age = request.form.get('age')
    calories = request.form.get('calories')
    packaging = request.form.get('packaging')
    weight_g = request.form.get('weight_g')

    food = Food.query.get(food_id)

    food.flavour = flavour
    food.wet_or_dry = wet_or_dry
    food.age = age
    food.calories = int(calories)
    food.packaging = packaging
    food.weight_g = int(weight_g)

    
    db.session.commit()
    
    return f'Food: {food.flavour} edited'

'''
Delete food routes
'''

@food.route('/delete/<int:food_id>/', methods=['DELETE'])
def delete_food(food_id):
    food = Food.query.get(food_id)
    db.session.delete(food)
    db.session.commit()

    return f'Food: {food.flavour} deleted'

