from flask_app.config.mysqlconnection import connectToMySQL

class User:

    db = 'friendships'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friends = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_by_id(cls, id):
        pass

    @classmethod
    def get_potential_friends(cls, data):
        pass

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO users (first_name, last_name)
            VALUES (%(first_name)s, %(last_name)s)
        '''
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id