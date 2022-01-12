from flask_app.config.mysqlconnection import connectToMySQL
class User:

    db = "users_cr"

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def create(cls, data) -> int:
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"        
        user_id = connectToMySQL(cls.db).query_db(query, data)
        return user_id

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)[0]
        return result

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id = %(user_id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s LIMIT 1;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result