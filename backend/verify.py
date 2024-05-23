import os
from backend.db_setup import SetUpMeals

def verify_db(db_name):
    db_exists = os.path.exists(db_name)
    if db_exists or len(db_name) == 0:
        return False, "Please pick a unique name for your calendar"
    else:
        return True, ""

def verify_email(email):
    if email[-10:] == "@gmail.com":
        return True, ""
    else:
        return False, "Please enter a gmail email."

def verify_ingredients(ingredients):
    if ',' not in ingredients:
        return False, "Please enter a comma separated list."
    parts = ingredients.split(',')
    if all(part.strip() for part in parts):
        return True, ""
    else:
        return False, "Please enter a comma separated list."


def verify_meal_name(name):
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
    if num_weeks.isdigit():
        return True, ""
    else:
        return False, "Please enter an integer."
    
def verify_num_meals():
    db = SetUpMeals()
    query = "select category from meals;"
    db.cursor.execute(query)
    db.connection.commit()
    rows = db.cursor.fetchall()
    
    if len(rows) < 3:
        return False, "Please enter at least one dish for each category."
        
    return True, ""