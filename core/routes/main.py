from flask import Blueprint, request

from ..models import User, Cat, owner_cat
from ..extensions import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return '<h1>Main route</h1>'

@main.route('/add-cat/', methods=['POST'])
def add_cat():
    user = User.query.get(1)
    weight = request.form.get('weight')
    weight_class = request.form.get('weight_class')
    is_neutered = False
    name = request.form.get('name')

    new_cat = Cat(
        weight=int(weight),
        weight_class=weight_class,
        is_neutered=is_neutered,
        name=name
    )

    db.session.add(new_cat)
    

    user.cats.append(Cat.query.get(1))

    db.session.commit()

    return 'Cat added'


