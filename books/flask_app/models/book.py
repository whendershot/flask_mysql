from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Book:

    db = 'books'

    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorited_by = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_by_id( cls, data):
        query = "SELECT * FROM books WHERE id = %(book_id)s LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query, data)[0]
        return results

    @classmethod
    def get_potential_books(cls, data):
        query = '''
            SELECT 
                * 
            FROM 
                books 
            WHERE
                id NOT IN (
                    SELECT book_id FROM favorites WHERE author_id = %(author_id)s
                );
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO books (title, num_of_pages)
            VALUES (%(title)s, %(num_of_pages)s)
        '''
        book_id = connectToMySQL(cls.db).query_db(query, data)
        return book_id

    @classmethod
    def update(cls, data):
        query = '''
            UPDATE books SET 
        '''

    @classmethod
    def delete(cls, id):
        pass