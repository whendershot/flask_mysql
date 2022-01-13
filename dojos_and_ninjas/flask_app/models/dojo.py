from flask_app.config.mysqlconnection import connectToMySQL

class Dojo:

    db = 'dojos_and_ninjas'


    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM dojos;'
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
    def create(cls, data):
        query = '''
            INSERT INTO dojos (name) 
            VALUES (%(name)s);
            '''
        
        dojo_id = connectToMySQL(cls.db).query_db(query, data)
        return dojo_id

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass
