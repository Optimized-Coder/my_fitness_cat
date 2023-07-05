import re
from .models import User

def get_daily_calories(weight_kg, is_neutered, weight_class):
    '''
    Function: calculates daily calorie intake for cats
    Parameters: 
    - int:weight_kg
    - bool:is_neutered 
    - str:weight_class
    Returns: daily calorie intake
        return type: int
    '''
    if not type(weight_kg) == int:
        raise TypeError("weight_class must be an integer")
    if not type(is_neutered) == bool:
        raise TypeError("is_neutered must be a boolean")
    if not type(weight_class) == str:
        raise TypeError("weight_class must be a string")

    base_calories = int(weight_kg) ** 0.75 * 70

    if is_neutered == True:
        base_calories *= 1.2
    else:
        base_calories *= 1.4

    if weight_class.lower() == 'overweight':
        base_calories *= 0.8
    elif weight_class.lower() == 'obese':
        base_calories *= 0.7
    elif weight_class.lower() == 'underweight':
        base_calories *= 1.2
    elif weight_class.lower() == 'normal':
        base_calories *= 1
    else:
        return 'Please enter a valid weight class'

    calories = round(base_calories)

    return calories

def validate_password(password):
    if len(password) < 8:
        print(len(password))
        return False
    elif not re.search(r'[a-z]', password):
        print('must include lowercase')
        return False
    elif not re.search(r'[A-Z]', password):
        print('must include uppercase')
        return False
    elif not re.search(r'\d', password):
        print('must include a number')
        return False
    elif not re.search(r'\W', password):
        print('must include a special character')
        return False
    else:
        print('password accepted')
        return True

def validate_email(email):
    if not re.search(r'@', email):
        return False
    elif bool(User.query.filter_by(email=email).first()):
        return False
    elif len(email) < 6:
        return False
    else:
        return True

def validate_username(username):
    if len(username) < 6:
        return False
    elif bool(User.query.filter_by(username=username).first()):
        return False
    else:
        return True