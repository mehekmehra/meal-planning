from flask import Flask, render_template, request, jsonify, session
from backend.db_setup import SetUpMeals
from backend.gcal import GCal
import csv
from backend.verify import verify_db, verify_email, verify_ingredients, verify_meal_name, verify_num_weeks

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/first_time')
def first_time():
    return render_template('first_time.html')

@app.route('/adding_meals')
def adding_meals():
    return render_template('adding_meals.html')

@app.route('/submit_info', methods=['POST'])
def get_new_info():
    data = request.get_json()
    db_name = data.get('name')
    email = data.get('email')

    is_valid, error_message = verify_db(db_name)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400
   
    is_valid, error_message = verify_email(email)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    # gc = GCal(1, True, calendar_name=db_name, db_name=db_name, user_email=email)
    # calendar_id = gc.calendar_id

    calendar_id = "testing"


    with open("user_info.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([db_name, email, calendar_id])
    
    print("first")
    session['db_name'] = db_name
    session['email'] = email
    session['calendar_id'] = calendar_id
    
    db = SetUpMeals(db_name, True)

    return jsonify({"status": "success", "message": error_message}), 400

# @app.route('/first_time', methods=['POST'])
# def get_first_time():
#     data = request.get_json()
#     is_first_time = data.get('is_first_time')
#     session['is_first_time'] = is_first_time
    
# @app.route('/returning_user', methods=['GET'])
# def returning_user():
#     db = SetUpMeals()
#     session['db_name'] = db.name

#     print(db.name)
#     return db.name

@app.route("/schedule_meals", methods=["Post"])
def schedule_meals():
    data = request.get_json()
    num_weeks_str = data.get('num_weeks')

    is_valid, error_message = verify_num_weeks(num_weeks_str)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400
    
    num_weeks = int(num_weeks_str)
    gc = GCal(num_weeks, False)

    gc.schedule_meals()
    return jsonify({"status": "success", "message": f"Calendar Made Successfully!"}), 200

@app.route('/submit_meal', methods=['POST'])
def get_meal():
    data = request.get_json()
    name = data.get('meal_name')
    ingredients = data.get('ingredients')
    category = data.get('category')
    
    is_valid, error_message = verify_ingredients(ingredients)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400
    
    is_valid, error_message = verify_meal_name(name)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    ingredients_list = ingredients.split(",")

    # add meal to database 
    db = SetUpMeals()
    db.addMeal(name, category, ingredients_list)
    db.verify()
    return name

if __name__ == '__main__':
    app.run(debug=True)
