from flask_app.config.mysql import connectToMySQL
from flask import flash
from flask_app.models import user

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books JOIN users on books.user_id = users.id;"
        results = connectToMySQL("books_schema").query_db(query)
        books = []
        for row in results:
            the_book = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            the_book.creator = user.User(user_data)
            books.append(the_book)
        return books

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM books JOIN users on books.user_id = users.id WHERE books.id = %(id)s;"
        result = connectToMySQL("books_schema").query_db(query,data)
        if not result:
            return False

        result = result[0]
        book = cls(result)
        data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "location": result['location'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        book.creator = user.User(data)
        return book

    @classmethod
    def add_book(cls, data):
        query = "INSERT INTO books (title, author, genre, user_id) VALUES (%(title)s, %(author)s, %(genre)s, %(user_id)s);"
        return connectToMySQL("books_schema").query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL("books_schema").query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title = %(title)s, author = %(author)s, genre = %(genre)s WHERE id = %(id)s;"
        return connectToMySQL("books_schema").query_db(query,data)

    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book['title']) < 1:
            flash("Title must be at least 1 character.")
            is_valid = False
        if len(book['author']) < 1:
            flash("Author must be at least 1 character.")
            is_valid = False
        if len(book['genre']) < 1:
            flash("Genre must be at least 1 character.")
            is_valid = False
        return is_valid

