from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class User:

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    PASSWORD_REGEX = re.compile(r'^.{8}$')

    db = 'login_site'
    
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.email_hash = data['email_hash']
        self.password_hash = data['password_hash']

    @staticmethod
    def validate(registrant):
        is_valid = True
        
        if (not User.EMAIL_REGEX.match(registrant['email'])):
            is_valid = False
            flash(f'Invalid email address: {registrant["email"]}', 'registration')
        
        if (not User.PASSWORD_REGEX.match(registrant['password'])):
            is_valid = False
            flash(f'Bad Password. Need at least length 8.', 'registration')

        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = '''
            SELECT *
            FROM users
            WHERE
                id = (SELECT user_id FROM users_pii WHERE email = %(email)s)
            LIMIT 1
        ;'''
        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return cls(result)

    @classmethod
    def is_unique(cls, data):
        query = '''
            SELECT id FROM users WHERE email_hash = %(email_hash)s LIMIT 1;
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) == 0

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO users 
            (
                email_hash,
                password_hash
            )
            VALUES 
            (
                %(email_hash)s,
                %(password_hash)s
            )
            ;'''
        
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id

    @classmethod
    def create_transaction(cls, data):
        '''Create a User into users and users_pii tables.'''

        query = '''
            BEGIN;
            INSERT INTO users
            (
                email_hash,
                password_hash
            )
            VALUES 
            (
                %(email_hash)s,
                %(password_hash)s
            );
            INSERT INTO users_pii 
            (
                user_id,
                first_name,
                last_name,
                birthday,
                age,
                email
            )
            VALUES 
            (
                %(user_id)s,
                %(first_name)s,
                %(last_name)s,
                %(birthday)s,
                %(age)s,
                %(email)s
            );
            COMMIT;
        '''
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
    def update(cls, data):
        query = '''
            UPDATE users
            SET 
                email_hash=%(email_hash)s,
                password_hash=%(password_hash)s,
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


class UserPII:

    db = 'login_site'
    
    def __init__(self, data):
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.birthday = data['birthday']
        self.age = data['age']
        self.email = data['email']

    @staticmethod
    def validate(registrant):
        is_valid = True
        
        if (not len(registrant['first_name']) > 2):
            is_valid = False
            flash(f'First Name needs at least 3 characters: {registrant["first_name"]}', 'registration')
        
        if (not UserPII.is_unique({'email' : registrant['email']})):
            is_valid = False
            flash(f'The address entered is already in use.  Please submit a different email.', 'registration')

        return is_valid

    @classmethod
    def is_unique(cls, data):
        query = '''
            SELECT user_id FROM users_pii WHERE email = %(email)s LIMIT 1;
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) == 0

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO users_pii 
            (
                user_id,
                first_name,
                last_name,
                birthday,
                age,
                email
            )
            VALUES 
            (
                %(user_id)s,
                %(first_name)s,
                %(last_name)s,
                %(birthday)s,
                %(age)s,
                %(email)s
            )
            ;'''
        
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id

    
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM users_pii
            ;'''

        results = connectToMySQL(cls.db).query_db(query)
        return results

    
    @classmethod
    def get_one(cls, data):
        query = '''
            SELECT * FROM users_pii WHERE user_id = %(user_id)s LIMIT 1;
            '''
        
        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE users_pii
            SET 
                first_name=%(salted_email)s,
                last_name=%(salt)s,
                birthday=%(salted_password)s,
                age=%(age)s,
                email=%(email)s,
                updated_at=NOW()
            WHERE 
                id = %(user_id)s 
            LIMIT 1
            ;'''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    
    @classmethod
    def delete(cls, data):
        query = '''
            DELETE FROM users 
            WHERE id = %(user_id)s 
            LIMIT 1
            ;'''

        result = connectToMySQL(cls.db).query_db(query, data)
        return result