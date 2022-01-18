from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author, book

class FavoriteBook:

    db = 'books'

    def __init__(self, data):
        self.author_id = data['author_id']
        self.book_id = data['book_id']

    @classmethod
    def get_all(cls):
        pass

    @classmethod
    def get_all_books(cls, data):
        query = '''
            SELECT * 
            FROM books 
            WHERE 
            id IN (
                SELECT book_id
                FROM favorites
                WHERE author_id = %(author_id)s
            )
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_all_authors(cls, data):
        query = '''
            SELECT * 
            FROM authors 
            WHERE 
            id IN (
                SELECT author_id
                FROM favorites
                WHERE book_id = %(book_id)s
            )
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO favorites (author_id, book_id)
            VALUES (%(author_id)s, %(book_id)s)
        '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result