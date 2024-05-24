import sqlite3
import csv

class SetUpMeals():
    def __init__(self, db_name=None, first_time=False):
        """ Initializes an object to interact with the database.
            Creates a database if it does not already exist and makes tables.
            If the database is not provided, it pulls the name from the user_info file.
            inputs
            ------
            db_name: name of the database as a string. Each database must have a unique name.
            first_time: boolean for whether this is the first time this database is being accessed.
        """
        if db_name:
            self.name = db_name
        else:
            with open("user_info.csv", mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    db_name = row[0]
                self.name = db_name

        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        if first_time:
            self.makeTables()

    def makeTables(self):
        """ Creats a meals table with columns name and category and a ingredients table
            with columns name and ingredient (where each row has the meal name and one ingredient).
        """
        make_meals_table ='''CREATE TABLE meals(
                name varchar(255) NOT NULL,
                category varchar(255)
                )'''
        self.cursor.execute(make_meals_table)

        make_ingredients_table ='''CREATE TABLE ingredients(
                name varchar(255) NOT NULL,
                ingredient varchar(255)
                )'''
        self.cursor.execute(make_ingredients_table)


    def addMeal(self, name, category, ingredients):
        """ Adds an inputted meal to the database. 
            In the meals table, adds the name and category.
            In the ingredients table, adds the name and a single ingredient per row.
            inputs
            ------
            name: name of the dish as a string.
            category: string which is one of "side", "protein" or "full_meal".
            ingredients: a list of each ingredient as a string.
            outputs
            -------
            last_row_id: the id of the last row that was accessed.
        """
        add_to_meals = ''' INSERT INTO meals(name, category)
              VALUES(?,?) '''
        
        self.cursor.execute(add_to_meals, (name, category))
        self.connection.commit()

        add_to_ingredients = ''' INSERT INTO ingredients(name, ingredient)
              VALUES(?,?) '''
        for ingredient in ingredients:
            self.cursor.execute(add_to_ingredients, (name, ingredient))
            self.connection.commit()

        return self.cursor.lastrowid
    
    def verify(self):
        """ Allows the user to verify the inputs in the tables by printing each table out.
        """
        sql = "SELECT * FROM meals;"
        self.cursor.execute(sql)
        self.connection.commit()
        rows = self.cursor.fetchall()
        print(len(rows))
        for row in rows:
            print(row)

        sql2 = "SELECT * FROM ingredients;"
        self.cursor.execute(sql2)
        self.connection.commit()
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
    
    def deleteMeal(self, name):
        """ Deletes the specified meal from the database, removing it from both tables.
            inputs
            ------
            name: the name of the meal to be deleted. 
        """
        delete_meals = "DELETE FROM meals WHERE name= ?;"
        delete_ingredients = "DELETE FROM ingredients WHERE name= ?;"
        self.cursor.execute(delete_meals, (name,))
        self.connection.commit()
        self.cursor.execute(delete_ingredients, (name,))
        self.connection.commit()

    def close(self):
        """ Closes the connection with the database.
        """
        self.connection.close()
