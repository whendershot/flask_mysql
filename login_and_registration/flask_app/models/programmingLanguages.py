from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class ProgrammingLanguages:

    db = 'login_site'
    
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.language = data['language']

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO programming_languages (language) 
            VALUES 
                (%(language)s),
            ;'''
        
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id

    
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM programming_languages
            ;'''

        results = connectToMySQL(cls.db).query_db(query)
        return results

    
    @classmethod
    def get_one(cls, data):
        query = '''
            SELECT * FROM programming_languages WHERE id = %(programming_language_id)s LIMIT 1;
            '''
        
        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE programming_languages
            SET 
                language=%(language)s,
                updated_at=NOW()
            WHERE 
                id = %(programming_language_id)s 
            LIMIT 1
            ;'''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    
    @classmethod
    def delete(cls, data):
        query = '''
            DELETE FROM programming_langauges 
            WHERE id = %(programming_language_id)s 
            LIMIT 1
            ;'''

        result = connectToMySQL(cls.db).query_db(query, data)
        return result

class LanguagesUsed:

    db = 'login_site'

    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.programming_language_id = data['programming_language_id']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO languages_used 
            (
                programming_language_id,
                user_id
            ) 
            VALUES 
            (
                %(programming_language_id)s,
                %(user_id)s
            )
            ;'''
        
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id

    
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM languages_used
            ;'''

        results = connectToMySQL(cls.db).query_db(query)
        return results

    
    @classmethod
    def get_by_language(cls, data):
        query = '''
            SELECT * FROM languages_used WHERE programming_language_id = %(programming_language_id)s;
            '''
        
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_by_user(cls, data):
        query = '''
            SELECT 
                *
            FROM
                languages_used
            LEFT JOIN
                programming_languages
            ON
                languages_used.programming_language_id = programming_languages.id
            WHERE
                languages_used.user_id = %(user_id)s
            ;
            '''
        
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE languages_used
            SET 
                programming_language_id = %(programming_language_id)s,
                user_id = %(user_id)s,
                updated_at = NOW()
            WHERE 
                id = %(id)s
            LIMIT 1
            ;'''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    
    @classmethod
    def delete(cls, data):
        query = '''
            DELETE FROM languages_used 
            WHERE id = %(id)s 
            LIMIT 1
            ;'''

        result = connectToMySQL(cls.db).query_db(query, data)
        return result