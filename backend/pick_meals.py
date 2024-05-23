from backend.db_setup import SetUpMeals
import random

class PickMeals():
    def __init__(self, db_name, num_weeks):
        self.db = SetUpMeals(db_name)
        self.num_weeks = num_weeks
    
    def categorize_meals(self):
        get_meals = """ SELECT meals.name, meals.category, ingredients.ingredient
        FROM meals
        LEFT JOIN ingredients ON meals.name = ingredients.name
        """
        self.db.cursor.execute(get_meals)
        rows = self.db.cursor.fetchall()

        meals_dict = {'side': [], 'protein': [], 'full_meal': []}
        ingredients_dict = {}

        for name, category, ingredient in rows:
            if name not in ingredients_dict:
                ingredients_dict[name] = {'category': category, 'ingredients': []}
            if ingredient:
                ingredients_dict[name]['ingredients'] += [ingredient]
       
        for name in ingredients_dict:
            category = ingredients_dict[name]['category']
            ingredients = ingredients_dict[name]['ingredients']

            meals_dict[category] += [(name, ingredients)]

        return meals_dict
    
    def pick_meal(self, meals_dict, category, previous_meals):
        available_meals = []
        for meal in meals_dict[category]:
            if meal[0] not in previous_meals:
                available_meals += [meal]

        # if the only meals in the category were already selected
        if not available_meals:
            available_meals = meals_dict[category]
        
        selected_meal = random.choice(available_meals)
        return selected_meal
    
    def meal_plan(self):
        meals_dict = self.categorize_meals()

        planned_meals = []
        previous_week_meals = set()

        for _ in range(self.num_weeks):
            random_int = random.randint(0, 2)
            curr_meals = []

            if random_int % 3 == 0:
                # one of each
                curr_meals += [self.pick_meal(meals_dict, 'side', previous_week_meals)]
                curr_meals += [self.pick_meal(meals_dict, 'protein', previous_week_meals)]
                curr_meals += [self.pick_meal(meals_dict, 'full_meal', previous_week_meals)]
            
            elif random_int % 3 == 1:
                # two proteins, two sides
                curr_meals += [self.pick_meal(meals_dict, 'side', previous_week_meals)]
                curr_meals += [self.pick_meal(meals_dict, 'protein', previous_week_meals)]

                # want to exclude the chosen meals for this week
                previous_week_meals.update([meal[0] for meal in curr_meals])
                curr_meals += [self.pick_meal(meals_dict, 'side', previous_week_meals)]
                curr_meals += [self.pick_meal(meals_dict, 'protein', previous_week_meals)]

            else:
                # two full_meals
                curr_meals += [self.pick_meal(meals_dict, 'full_meal', previous_week_meals)]

                # want to exclude the chosen meals for this week
                previous_week_meals.update([meal[0] for meal in curr_meals])
                curr_meals += [self.pick_meal(meals_dict, 'full_meal', previous_week_meals)]

            planned_meals += [curr_meals]
            previous_week_meals = set(meal[0] for meal in curr_meals)

        return planned_meals



    




