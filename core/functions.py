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

