from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:

    db = 'books'

    def __init__( self , data ):
        self.id = data['id']
        self.title = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM authors;
        '''
        result = connectToMySQL(cls.db).query_db(query)
        return result

    @classmethod
    def get_by_id( cls, data):
        query = '''
            SELECT * FROM authors WHERE id = %(author_id)s LIMIT 1;
        '''
        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    @classmethod
    def get_potential_authors(cls, data):
        query = '''
            SELECT
                *
            FROM
                authors
            WHERE 
                id NOT IN (
                    SELECT author_id FROM favorites WHERE book_id = %(book_id)s
                );
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO authors (name)
            VALUES (%(author_name)s)
        '''
        _author_id = connectToMySQL(cls.db).query_db(query, data)
        return _author_id

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, id):
        pass