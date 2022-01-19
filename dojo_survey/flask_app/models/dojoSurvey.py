from flask_app.config.mysqlconnection import connectToMySQL

class DojoSurvey:

    db = 'dojo_survey'

    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comment = data['comment']

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO dojos (name, location, language, comment)
            VALUES (
                %(name)s,
                %(location)s,
                %(language)s,
                %(comment)s
            )
        '''
        row_id = connectToMySQL(cls.db).query_db(query, data)
        return row_id

    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM dojos;'''
        results = connectToMySQL(cls.db).query_db(query)
        surveys = []
        for i in results:
            surveys.append(cls(i))
        return surveys

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass