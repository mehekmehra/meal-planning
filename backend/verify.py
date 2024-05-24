import os
from backend.db_setup import SetUpMeals

def verify_db(db_name):
    """ checks if a database name is valid (does not exist already).
        inputs
        ------
        db_name: name of a database as a string.
        outputs
        -------
        tuple of boolean for if the database name is valid and an error message.
    """
    db_exists = os.path.exists(db_name)
    if db_exists or len(db_name) == 0:
        return False, "Please pick a unique name for your calendar"
    return True, ""


def verify_email(email):
    """ checks if the email address is valid. 
        inputs
        ------
        email: email address as a string.
        outputs
        -------
        tuple of boolean for if the email address is valid and an error message.
    """
    if email[-10:] == "@gmail.com":
        return True, ""
    return False, "Please enter a gmail email."


def verify_ingredients(ingredients):
    """ checks if the ingredients list is comma separated and therefore, valid. 
        inputs
        ------
        ingredients: a string of ingredients.
        outputs
        -------
        tuple of boolean for if the ingredients format is valid and an error message.
    """
    if ',' not in ingredients:
        return False, "Please enter a comma separated list."
    parts = ingredients.split(',')
    if all(part.strip() for part in parts):
        return True, ""
    return False, "Please enter a comma separated list."


def verify_meal_name(name):
    """ checks if the email address is valid. 
        inputs
        ------
        email: email address as a string.
        outputs
        -------
        tuple of boolean for if the email address is valid and an error message.
    """
    db = SetUpMeals()
    query = "select name from meals;"
    db.cursor.execute(query)
    db.connection.commit()
    rows = db.cursor.fetchall()

    if len(name) == 0:
        return False, "Please enter a name for your meal."
    for row in rows:
        if (name,) == row:
            return False, "Please enter a unique name for your meal."
    return True, ""


def verify_num_weeks(num_weeks):
    """ checks if the number of weeks includes digits and is therefore valid. 
        inputs
        ------
        num_weeks: a string.
        outputs
        -------
        tuple of boolean for if the string only includes digits and an error message.
    """
    if num_weeks.isdigit():
        return True, ""
    return False, "Please enter an integer."


def verify_num_meals():
    """ checks if there are enough meals in the database. 
        outputs
        -------
        tuple of boolean for if there are enough meals in each category and an error message.
    """
    db = SetUpMeals()
    query = "select category from meals;"
    db.cursor.execute(query)
    db.connection.commit()
    rows = db.cursor.fetchall()

    if len(rows) < 3:
        return False, "Please enter at least one dish for each category."

    return True, ""
