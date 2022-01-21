from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User:

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*[0-9]).{8}$')

    db = 'recipes'
    
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password_hash = data['password_hash']

    @staticmethod
    def validate(registrant):
        is_valid = True
        
        if (not User.EMAIL_REGEX.match(registrant['email'])):
            is_valid = False
            flash(f'Invalid email address: {registrant["email"]}', 'registration')
        
        if (not User.is_unique({'email' : registrant['email']})):
            is_valid = False
            flash(f'The address entered is already in use.  Please submit a different email.', 'registration')

        if (not User.PASSWORD_REGEX.match(registrant['password'])):
            is_valid = False
            flash(f'Bad Password. Need at least: length 8, 1 upper case, 1 number.', 'registration')

        if (not len(registrant['first_name']) >= 2):
            is_valid = False
            flash(f'First Name needs at least 2 characters: {registrant["first_name"]}', 'registration')
        
        if (not len(registrant['last_name']) >= 2):
            is_valid = False
            flash(f'First Name needs at least 2 characters: {registrant["first_name"]}', 'registration')

        if (not registrant['password'] == registrant['password_confirm']):
            is_valid = False
            flash(f'Must confirm password.', 'registration')

        return is_valid

    @classmethod
    def is_unique(cls, data):
        query = '''
            SELECT id FROM users WHERE email = %(email)s LIMIT 1;
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) == 0

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO users 
            (
                first_name,
                last_name,
                email,
                password_hash
            )
            VALUES 
            (
                %(first_name)s,
                %(last_name)s,
                %(email)s,
                %(password_hash)s
            )
            ;'''
        
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id


    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM users
            ;'''

        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_one(cls, data):
        query = '''
            SELECT * FROM users WHERE id = %(id)s LIMIT 1;
            '''

        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    @classmethod
    def get_by_email(cls, data):
        query = '''
            SELECT 
                *
            FROM 
                users
            WHERE
                email = %(email)s
            LIMIT 1
        ;'''
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]

    classmethod
    def update(cls, data):
        query = '''
            UPDATE users
            SET 
                first_name = %(first_name)s, 
                last_name = %(last_name)s,
                email = %(email)s,
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
            DELETE FROM users 
            WHERE id = %(id)s 
            LIMIT 1
            ;'''

        result = connectToMySQL(cls.db).query_db(query, data)
        return result