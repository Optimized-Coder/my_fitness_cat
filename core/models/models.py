from ..extensions import db
from flask_login import UserMixin

from datetime import datetime, date

owner_cat = db.Table(
    'owner_cat',
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('cat_id', db.Integer, db.ForeignKey('cat.id'))
)

cat_food = db.Table(
    'cat_food',
    db.Column('cat_id', db.Integer, db.ForeignKey('cat.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(24), default='User')
    last_name = db.Column(db.String(24), default='Name')
    password_hash = db.Column(db.String(128), nullable=False)
    cats = db.relationship('Cat', secondary=owner_cat, backref='owner', lazy='dynamic')
    
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
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date)
    breed = db.Column(db.String(80), default='N/A')
    color = db.Column(db.String(80), default='N/A')
    weight = db.Column(db.Float, default=3)
    weight_class = db.Column(db.String(24), default='normal')
    is_neutered = db.Column(db.Boolean, default=True)
    food_choice = db.relationship('Food',
    secondary=cat_food, backref='cat', lazy='dynamic'
    )

    def __repr__(self):
        return f'{self.id}: {self.name}'
    
    @property
    def age(self):
        return int(datetime.now().year) - int(self.dob.year)

    @property
    def age_months(self):
        return self.age * 12 + (int(datetime.now().month) - int(self.dob.month))


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

        coefficient = 1

        if self.age_months >= 12:
            if self.is_neutered == True:
                coefficient *= 1.6
            else:
                coefficient *= 1.8
        else:
            coefficient *= 1

        if self.weight_class.lower() == 'overweight':
            coefficient *= 0.8
        elif self.weight_class.lower() == 'underweight':
            coefficient *= 1.2
        else:
            coefficient *= 1

        if self.age_months <= 4:
            coefficient *= 3
        elif self.age_months > 4 and self.age_months < 12:
            coefficient *= 2
        else:
            coefficient *= 1

        calories = round(base_calories * coefficient)

        return calories
    
    @property
    def grams_of_dry(self):
        calorie_requirement = int(self.daily_calories)
        CALORIES_PER_100_GRAMS = 377

        grams_of_dry = round(calorie_requirement / CALORIES_PER_100_GRAMS * 100)

        return grams_of_dry
    
    @property
    def grams_of_wet(self):
        calorie_requirement = int(self.daily_calories)
        CALORIES_PER_100_GRAMS = 73

        grams_of_wet = round(calorie_requirement / CALORIES_PER_100_GRAMS * 100)

        return grams_of_wet
    
    @property
    def grams_of_chosen_food(self):
        calorie_requirement = int(self.daily_calories)
        if self.food_choice.count() > 0:
            CALORIES_PER_100_GRAMS = self.food_choice[0].calories
            grams_of_chosen_food = round(calorie_requirement / CALORIES_PER_100_GRAMS * 100)
            
            return grams_of_chosen_food
        else:
            return 0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': str(self.dob),
            'breed': self.breed,
            'color': self.color,
            'weight': self.weight,
            'weight_class': self.weight_class,
            'is_neutered': self.is_neutered,
            'daily_calories': self.daily_calories,
            'grams_of_dry': self.grams_of_dry,
            'grams_of_wet': self.grams_of_wet, 
            'age': self.age,
            'age_months': self.age_months,
            'food_choice': [food.to_dict() for food in self.food_choice],
            'grams_of_chosen_food': self.grams_of_chosen_food
        }

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wet_or_dry = db.Column(db.String(8), index=True)
    flavour = db.Column(db.String(24), index=True)
    age = db.Column(db.String, index=True)
    # calories per 100g
    calories = db.Column(db.Integer)
    packaging = db.Column(db.String, index=True)
    weight_g = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'wet_or_dry': self.wet_or_dry,
            'flavour': self.flavour,
            'age': self.age,
            'calories': self.calories,
            'packaging': self.packaging,
            'weight_grams': f'{self.weight_g}g'
        }