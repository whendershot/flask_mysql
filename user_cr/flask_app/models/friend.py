# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
class Friend:

    db = "first_flask"

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.occupation = data['occupation']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM friends;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of friends
        friends = []
        # Iterate over the db results and create instances of friends with cls.
        for friend in results:
            friends.append( cls(friend) )
        return friends

    @classmethod
    def add_friend(cls, data) -> int:
        query = "INSERT INTO first_flask.friends (first_name, last_name, occupation) VALUES (%(first_name)s, %(last_name)s, %(occupation)s);"        
        friend_id = connectToMySQL(cls.db).query_db(query, data)
        return friend_id
