from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.dojo import Dojo

class Ninja:

    db = 'dojos_and_ninjas'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.dojo_id = data['dojo_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM ninjas;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        ninjas = []
        for ninja in results:
            ninjas.append(ninja)
        return results

    @classmethod
    def get_one(cls, id):
        pass

    @classmethod
    def get_all_by_dojo_id(cls, dojo_id):
        query = 'SELECT * FROM ninjas WHERE dojo_id = %(dojo_id)s'
        data = {
            'dojo_id' : dojo_id
        }
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO ninjas (first_name, last_name, age, dojo_id)
            VALUES (
                %(first_name)s,
                %(last_name)s,
                %(age)s,
                %(dojo_id)s
            );
        '''
        ninja_id = connectToMySQL(cls.db).query_db(query, data)
        return ninja_id

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass
