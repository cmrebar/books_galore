from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash, request
bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.books = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password)VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL("books_galore").query_db(query,data)
    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("books_galore").query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("books_galore").query_db(query,data)
        if not result:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query ="SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("books_galore").query_db(query,data)
        if not result:
            return False

        return cls(result[0])
    
    @staticmethod
    def validate_reg(data):
        valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long.","register")
            valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long.","register")
            valid = False
        if len(data['email']) < 1:
            flash("Email cannot be blank.","register")
            valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.","register")
            valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long.","register")
            valid = False
        if data['password'] != data['confirm']:
            flash("Passwords do not match.","register")
            valid = False
        return valid
    
    @staticmethod
    def validate_login(data):
        user = User.get_by_email(data['email'])
        if not user:
            flash("Invalid email/password.","login")
            return False
        if not bcrypt.check_password_hash(user.password,data['password']):
            flash("Invalid email/password.","login")
            return False
        return user
