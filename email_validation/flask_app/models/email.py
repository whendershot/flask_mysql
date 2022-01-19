from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Email:

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    db = 'email_validation'
    
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.email = data['email']

    @staticmethod
    def validate_email(email):
        is_valid = True
        
        if (not Email.EMAIL_REGEX.match(email['email'])):
            is_valid = False
            flash(f'Invalid email address: {email["email"]}', 'email')
        
        if (not Email.is_unique({'email' : email['email']})):
            is_valid = False
            flash(f'The address entered is already in use.  Please submit a different email.', 'email')

        if (is_valid):
            flash(f'The email address you entered ({email["email"]}) is a VALID email address!  Thank you!', 'success')
        return is_valid

    @classmethod
    def is_unique(cls, data):
        query = '''
            SELECT id FROM emails WHERE email = %(email)s LIMIT 1;
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) == 0

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO emails (email) 
            VALUES (%(email)s);
            '''
        
        dojo_id = connectToMySQL(cls.db).query_db(query, data)
        return dojo_id

    
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM emails
            ;'''

        results = connectToMySQL(cls.db).query_db(query)
        return results

    
    @classmethod
    def get_one(cls, data):
        query = '''
            SELECT * FROM dojos WHERE dojos.id = %(dojo_id)s LIMIT 1;
            '''
        
        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE emails
            SET 
                email=%(email)s,
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
            DELETE FROM emails 
            WHERE id = %(id)s 
            LIMIT 1
            ;'''

        result = connectToMySQL(cls.db).query_db(query, data)
        return result