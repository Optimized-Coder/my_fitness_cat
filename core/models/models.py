from ..extensions import db
from flask_login import UserMixin

owner_cat = db.Table(
    'owner_cat',
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('cat_id', db.Integer, db.ForeignKey('cat.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    password_hash = db.Column(db.String(128))
    cats = db.relationship('Cat', secondary=owner_cat, backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'{self.id}: {self.first_name}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'cats': [cat.to_dict() for cat in self.cats]
        }
    
class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer)
    breed = db.Column(db.String(80))
    color = db.Column(db.String(80))
    weight = db.Column(db.Integer)
    weight_class = db.Column(db.String(24))
    is_neutered = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.id}: {self.name}'

    @property
    def daily_calories(self):
        '''
        Function: calculates daily calorie intake for cats
        Parameters: 
        - int:weight_kg
        - bool:is_neutered 
        - str:weight_class
        Returns: daily calorie intake
            return type: int
        '''

        base_calories = self.weight ** 0.75 * 70

        if self.is_neutered == True:
            base_calories *= 1.2
        else:
            base_calories *= 1.4

        if self.weight_class.lower() == 'overweight':
            base_calories *= 0.8
        elif self.weight_class.lower() == 'obese':
            base_calories *= 0.7
        elif self.weight_class.lower() == 'underweight':
            base_calories *= 1.2
        elif self.weight_class.lower() == 'normal':
            base_calories *= 1
        else:
            return 'Please enter a valid weight class'

        calories = round(base_calories)

        return calories

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'breed': self.breed,
            'color': self.color,
            'weight': self.weight,
            'weight_class': self.weight_class,
            'is_neutered': self.is_neutered,
            'daily_calories': self.daily_calories
        }