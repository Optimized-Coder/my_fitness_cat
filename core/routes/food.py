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
    age = request.form.get('age')
    calories = request.form.get('calories')
    packaging = request.form.get('packaging')

    food = Food(
        flavour=flavour,
        age=age,
        calories=calories,
        packaging=packaging
    )

    db.session.add(food)
    db.session.commit()

    return f'Food: {food.flavour} added'

'''
View food routes
'''

@food.route('/view/json/', methods=['GET'])
def view_food_json():
    foods = Food.query.all()

    return [jsonify(food.to_dict()) for food in foods]

@food.route('/view/', methods=['GET'])
def view_food():
    foods = Food.query.all()

    context = {
        'title': 'View Food',
        'foods': foods
    }

    return render_template(
        'food/view.html',
        **context
    )

'''
Edit food routes
'''

@food.route('/edit/<int:id>/', methods=['GET'])
def edit_food_get(food_id):
    food = Food.query.get(food_id)

    context = {
        'title': 'Edit Food',
        'food': food
    }

    return render_template(
        'food/edit.html',
        **context
    )

@food.route('/edit/<int:id>/', methods=['POST'])
def edit_food(food_id):
    flavour = request.form.get('flavour')
    age = request.form.get('age')
    calories = request.form.get('calories')
    packaging = request.form.get('packaging')

    food = Food.query.get(food_id)

    food.flavour = flavour
    food.age = age
    food.calories = calories
    food.packaging = packaging
    
    db.session.commit()
    
    return f'Food: {food.flavour} edited'

'''
Delete food routes
'''

@food.route('/delete/<int:id>/', methods=['GET'])
def delete_food_get(food_id):
    food = Food.query.get(food_id)

    context = {
        'title': 'Delete Food',
        'food': food
    }
    
    return render_template(
        'food/delete.html',
        **context
    )

@food.route('/delete/<int:id>/', methods=['DELETE'])
def delete_food(food_id):
    food = Food.query.get(food_id)
    db.session.delete(food)
    db.session.commit()

    return f'Food: {food.flavour} deleted'

