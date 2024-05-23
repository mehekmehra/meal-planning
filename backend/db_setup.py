import sqlite3
import csv

class SetUpMeals():
    def __init__(self, db_name=None, first_time=False):
      
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
        sql = "select * from meals;"
        self.cursor.execute(sql)
        self.connection.commit()
        rows = self.cursor.fetchall()
        print(len(rows))
        for row in rows:
            print(row)

        sql2 = "select * from ingredients;"
        self.cursor.execute(sql2)
        self.connection.commit()
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
    
    def deleteMeal(self, name):
        delete_meals = "DELETE FROM meals WHERE name= ?;"
        delete_ingredients = "DELETE FROM ingredients WHERE name= ?;"
        self.cursor.execute(delete_meals, (name,))
        self.connection.commit()
        self.cursor.execute(delete_ingredients, (name,))
        self.connection.commit()

    def close(self):
        self.connection.close()
