from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash

class User:
    def __init__(self, data):
        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls,data):
        hashed_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': bcrypt.generate_password_hash(data['password'].encode('utf-8')),
        }
        query = """
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """
        return connectToMySQL("websighting").query_db(query,hashed_data)
    
    @classmethod
    def get_by_email(cls, email):
        data={"email": email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("websighting").query_db(query,data)
        if not result:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query ="SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("websighting").query_db(query,data)
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
