from flask_app.config.mysqlconnection import connectToMySQL

class Friendship:

    db = 'friendships'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = '''
            SELECT 
                users.id AS user_id,
                CONCAT(users.first_name, ' ', users.last_name) AS user_name,
                friends.id AS friend_id,
                CONCAT(friends.first_name, ' ', friends.last_name) AS friend_name
            FROM 
                users AS users
            
            LEFT JOIN
            (
                SELECT
                    friend_id,
                    user_id
                FROM
                    friendships
            ) AS friendships
            ON
                users.id = friendships.user_id

            LEFT JOIN
            (
                SELECT
                    id,
                    first_name,
                    last_name
                FROM
                    users
            ) AS friends
            ON
                friendships.friend_id = friends.id
            ;'''
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def get_by_id(cls, id):
        pass

    @classmethod
    def get_potential_friends(cls, data):
        query = '''
                SELECT
                    id,
                    first_name,
                    last_name
                FROM
                    users
                WHERE id NOT IN (
                    SELECT 
                        friend_id 
                    FROM 
                        friendships 
                    WHERE 
                        user_id = %(user_id)s 
                    UNION (SELECT %(user_id)s AS friend_id) 
                )
            ;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO friendships (user_id, friend_id)
            SELECT %(user_id)s, %(friend_id)s
            FROM DUAL
            WHERE NOT EXISTS(
                    SELECT
                        user_id,
                        friend_id
                    FROM
                        friendships
                    WHERE
                        user_id = %(user_id)s AND friend_id = %(friend_id)s
                )
            ;
        '''
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id