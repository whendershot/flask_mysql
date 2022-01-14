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
        pass

    @classmethod
    def get_one( cls, id):
        pass

    @classmethod
    def create(cls, data):
        pass

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, id):
        pass