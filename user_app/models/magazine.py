from user_app.models import user
from user_app.static.regex import ALPHA_SPACE_SYMBOLS
from user_app.config.mysqlconnection import queryMySQL
from flask import flash

class Magazine:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.description = data["description"]

    @classmethod
    def create(cls, data):
        query = "INSERT INTO magazines (name, user_id, description) VALUES (%(name)s, %(user_id)s, %(description)s);"
        queryMySQL(query, data)

    @classmethod
    def get_by_id(cls, id):
        query = f"SELECT * FROM magazines WHERE id = {id}"
        magazine = cls(queryMySQL(query)[0])
        magazine.owner = user.User.get_by_id({"id": magazine.user_id})
        return magazine

    @classmethod
    def get_all(cls):
        magazines = []
        query = "SELECT * FROM magazines JOIN users ON users.id = magazines.user_id;"
        results = queryMySQL(query)
        for result in results:
            temp_magazine = cls(result)
            temp_magazine.owner = user.User.get_by_id({"id": result["users.id"]})
            magazines.append(temp_magazine)
        return magazines

    
    @staticmethod
    def delete(id):
        query = f"DELETE FROM magazines WHERE id = {id}"
        queryMySQL(query)

    @staticmethod
    def validate_new(magazine):
        is_valid = True
        if not ALPHA_SPACE_SYMBOLS.match(magazine["name"]):
            flash("Name may only contain alphanumeric characters")
            is_valid = False
        elif len(magazine["name"]) < 2:
            flash("Name must be at least 2 characters long")
            is_valid = False
        if len(magazine["description"]) < 10:
            flash("Description must be at least 10 characters")
            is_valid = False
        return is_valid