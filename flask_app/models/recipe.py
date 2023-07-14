from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db_name = 'recipes_schema'


class Recipe:
    def __init__(self, db_data):
        # Constructor to initialize the Recipe object with data from the database
        # Each attribute represents a column in the 'recipes' table
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.under30 = db_data['under30']
        self.date_made = db_data['date_made']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls, data):
        # Method to insert a new recipe into the 'recipes' table
        query = "INSERT INTO recipes (name, description, instructions, under30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        # Method to retrieve all recipes from the 'recipes' table and join with 'users' table
        query = """SELECT * FROM recipes JOIN users ON
                    users.id = recipes.user_id;"""
        results = connectToMySQL(db_name).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            recipe_user = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            recipe.user = user.User(recipe_user)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one(cls, data):
        # Method to retrieve a single recipe from the 'recipes' table based on its id
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        # Method to update a recipe in the 'recipes' table
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, date_made = %(date_made)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        # Method to delete a recipe from the 'recipes' table
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        # Static method to validate recipe data before saving or updating
        is_valid = True
        if len(recipe['name']) < 2:
            is_valid = False
            flash("Name is required to be at least 2 characters", "recipe")
        if len(recipe['description']) < 2:
            is_valid = False
            flash("Description is required to be at least 2 characters", "recipe")
        if len(recipe['instructions']) < 2:
            is_valid = False
            flash("Instructions is required to be at least 2 characters", "recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date", "recipe")
        return is_valid
