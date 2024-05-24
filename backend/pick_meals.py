from backend.db_setup import SetUpMeals
import random

class PickMeals():
    def __init__(self, db_name, num_weeks):
        """ Creates a meal picking object. 
            inputs
            ------
            db_name: name of the database as a string.
            num_weeks: the number of weeks meals need to be picked for as an integer.
        """
        self.db = SetUpMeals(db_name)
        self.num_weeks = num_weeks

    def categorize_meals(self):
        """ Organizes the meals in the database by category and returns them as a dictionary.
            outputs
            -------
            meals_dict: dictionary where the keys are the categories "side", "protein", "full_meal"
                        and the values tuples of the dish name and the list of ingredients.
        """
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
        """ picks a single meal based on the dictionary, category and previous meals. 
            Picks a meal from the specified category and avoids previous_meals. If no other meal 
            options are available, picks a previous_meal.
            inputs
            ------
            meals_dict: dictionary output of categorize_meals.
            category: string: one of: "side", "protein", "full_meal".
            previous_meals: a list of names of meals. 
            outputs
            -------
            selected_meal: the chosen meal. Tuple: (meal_name, ingredients_list).
        """
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
        """ Plans the meals for self.num_weeks as a list of lists, where each sublist are the meals 
            for one week.
            outputs
            -------
            planned_meals: list of lists of meals.
                           [[("meal1", ["ingredient1", ...]), ("meal2", ["ingredient2, ..."])], ...]
        """
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
