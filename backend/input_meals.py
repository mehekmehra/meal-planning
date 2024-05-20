from backend.db_setup import MakeDB

class Meal():
    def __init__(self, name, category, ingredients):
        """ creates a meal object 
            inputs:
            name: name of the dish
            category: one of: "side", "protein" or "full_meal"
            ingredients: list of ingredients.
        """
        self.name = name
        self.category = category
        self.ingredients = ingredients
    