from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:

    db = 'recipes'
    
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.is_under_30_minutes = data['is_under_30_minutes']
        self.made_on = data['made_on']
        self.owned_by_user_id = data['owned_by_user_id']

    @staticmethod
    def validate(recipe):
        is_valid = True
        
        if (not len(recipe['name']) >= 3):
            is_valid = False
            flash(f'Recipe name needs at least 3 characters: {recipe["name"]}', 'create_recipe')
        
        if (not len(recipe['description']) >= 3):
            is_valid = False
            flash(f'Description needs at least 3 characters: {recipe["description"]}', 'create_recipe')
        
        if (not len(recipe['instructions']) >= 3):
            is_valid = False
            flash(f'Insructions need to be at least 3 characters: {recipe["instructions"]}', 'create_recipe')

        if (recipe['made_on'] == ''):
            is_valid = False
            flash(f'You need to enter a day that this recipe was last made', 'create_recipe')

        return is_valid

    @staticmethod
    def is_owner(data):
        _recipe = Recipe.get_one({'id' : data['recipe_id']})
        return data['user_id'] == _recipe['owned_by_user_id']


    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO recipes
            (
                name,
                description,
                instructions,
                is_under_30_minutes,
                made_on,
                owned_by_user_id
            )
            VALUES 
            (
                %(name)s,
                %(description)s,
                %(instructions)s,
                %(is_under_30_minutes)s,
                %(made_on)s,
                %(user_id)s
            )
            ;'''
        
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id


    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM recipes
            ;'''

        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_one(cls, data):
        query = '''
            SELECT * FROM recipes WHERE id = %(id)s LIMIT 1;
            '''

        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    @classmethod
    def update(cls, data):
        query = '''
            UPDATE recipes
            SET 
                name = %(name)s, 
                description = %(description)s,
                instructions = %(instructions)s,
                is_under_30_minutes = %(is_under_30_minutes)s,
                made_on = %(made_on)s,
                updated_at=NOW()
            WHERE 
                id = %(id)s 
            LIMIT 1
            ;'''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    
    @classmethod
    def delete(cls, data):
        query = '''
            DELETE FROM recipes 
            WHERE id = %(id)s 
            LIMIT 1
            ;'''

        result = connectToMySQL(cls.db).query_db(query, data)
        return result