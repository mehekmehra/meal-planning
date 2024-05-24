import csv
from flask import Flask, render_template, request, jsonify, session
from backend.db_setup import SetUpMeals
from backend.gcal import GCal
from backend import verify


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    """ Routes to the home page.
    """
    return render_template('index.html')

@app.route('/first_time')
def first_time():
    """ Routes to the first time user page.
    """
    return render_template('first_time.html')

@app.route('/adding_meals')
def adding_meals():
    """ Routes to the adding meals page.
    """
    return render_template('adding_meals.html')

@app.route('/submit_info', methods=['POST'])
def get_new_info():
    """ Gets the user info from the form on the webpage. Gets a name for the calendar and database
        and a email address.
        Initializes a GCal object, which creates a calendar and shares it with the email.
        Adds the database name, email address and calendar id to user_info.csv.
        outputs
        -------
        json messages for either successful inputs or errors that will be displayed on the webpage.
    """
    data = request.get_json()
    db_name = data.get('name')
    email = data.get('email')

    is_valid, error_message = verify.verify_db(db_name)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    is_valid, error_message = verify.verify_email(email)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    gc = GCal(1, True, calendar_name=db_name, user_email=email)
    calendar_id = gc.calendar_id

    # calendar_id = "testing"

    with open("user_info.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([db_name, email, calendar_id])

    session['db_name'] = db_name
    session['email'] = email
    session['calendar_id'] = calendar_id

    db = SetUpMeals(db_name, True)
    db.close()

    return jsonify({"status": "success", "message": "User Info Added!"}), 400


@app.route("/schedule_meals", methods=["Post"])
def schedule_meals():
    """ Creates a meal schedule for the number of weeks entered and the database of meals.
        Populates them in the calendar initialized for the user. 
        outputs
        -------
        json messages for either successful inputs or errors that will be displayed on the webpage.
    """
    data = request.get_json()
    num_weeks_str = data.get('num_weeks')

    is_valid, error_message = verify.verify_num_weeks(num_weeks_str)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    is_valid, error_message = verify.verify_num_meals()
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    num_weeks = int(num_weeks_str)
    gc = GCal(num_weeks, False)

    gc.schedule_meals()
    return jsonify({"status": "success", "message": "Calendar Made Successfully!"}), 200

@app.route('/submit_meal', methods=['POST'])
def get_meal():
    """ Adds a meal to the database based on the name, ingredients and category. 
        outputs
        -------
        json messages for either successful inputs or errors that will be displayed on the webpage.
    """
    data = request.get_json()
    name = data.get('meal_name')
    ingredients = data.get('ingredients')
    category = data.get('category')

    is_valid, error_message = verify.verify_ingredients(ingredients)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    is_valid, error_message = verify.verify_meal_name(name)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    ingredients_list = ingredients.split(",")

    # add meal to database 
    db = SetUpMeals()
    db.addMeal(name, category, ingredients_list)
    db.verify()
    db.close()
    return jsonify({"status": "success", "message": "Meal Added!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
