from user_app.models import magazine
from user_app.static.regex import ALPHA_SPACE, EMAIL
from user_app.config.mysqlconnection import queryMySQL
from flask import flash

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return queryMySQL(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        queryMySQL(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        return cls(queryMySQL(query, data)[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = queryMySQL(query, data)
        if result:
            return cls(result[0])
    
    @staticmethod
    def get_user_magazines(user_id):
        magazines = []
        query = f"SELECT * FROM magazines WHERE user_id = {user_id};"
        results = queryMySQL(query)
        for result in results:
            magazines.append(magazine.Magazine(result))
        return magazines

    @staticmethod
    def validate_new(user):
        is_valid = True
        if not ALPHA_SPACE.match(user["first_name"]):
            flash("First name may only contain alphanumeric characters")
            is_valid = False
        elif len(user["first_name"]) < 2:
            flash("First name must be at least two characters")
            is_valid = False
        if not ALPHA_SPACE.match(user["last_name"]):
            flash("Last name may only contain alphanumeric characters")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least two characters")
            is_valid = False
        if len(user["email"]) < 5:
            flash("Email must be at least five characters")
            is_valid = False
        elif not EMAIL.match(user["email"]):
            flash("Invalid Email Address")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters long")
            is_valid = False
        if user["confirm_password"] != user["password"]:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True
        if not ALPHA_SPACE.match(user["first_name"]):
            flash("First name may only contain alphanumeric characters")
            is_valid = False
        elif len(user["first_name"]) < 2:
            flash("First name must be at least two characters")
            is_valid = False
        if not ALPHA_SPACE.match(user["last_name"]):
            flash("Last name may only contain alphanumeric characters")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least two characters")
            is_valid = False
        if len(user["email"]) < 5:
            flash("Email must be at least five characters")
            is_valid = False
        elif not EMAIL.match(user["email"]):
            flash("Invalid Email Address")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user["email"]) < 5:
            flash("Email must be at least five characters")
            is_valid = False
        elif not EMAIL.match(user["email"]):
            flash("Invalid Email Address")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        return is_valid

    @staticmethod
    def check_unique(data):
        is_unique = True
        results = queryMySQL("SELECT * FROM users;")
        for result in results:
            if result["email"] == data["email"]:
                flash("Email has already been registered")
                is_unique = False
                return is_unique
        return is_unique
