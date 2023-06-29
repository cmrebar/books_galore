from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import review

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.genre = data['genre']
        self.cover_image = data['cover_image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.reviews = []
        self.creator = None

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM books JOIN users on books.user_id = users.id;"
        results = connectToMySQL("books_galore").query_db(query)
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
        result = connectToMySQL("books_galore").query_db(query,data)
        if not result:
            return False

        result = result[0]
        book = cls(result)
        book.creator = user.User.get_by_id({"id": result['users.id']})
        return book

    @classmethod
    def get_book_with_reviews(cls,data):
        query = "SELECT * FROM books LEFT JOIN reviews on books.id = reviews.book_id WHERE books.id = %(id)s;"
        results = connectToMySQL("books_galore").query_db(query,data)
        if not results:
            return False
        book = cls(results[0])
        print(results)
        print(book.reviews)
        for row in results:
            review_data = {
                "id": row['reviews.id'],
                "content": row['content'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
                "user_id": row['reviews.user_id'],
                "book_id": row['book_id']
            }
            book.reviews.append(review.Review(review_data))
        return book
    
    @classmethod
    def get_by_title(cls,data):
        query = "SELECT * FROM books WHERE books.title = %(title)s;"
        result = connectToMySQL("books_galore").query_db(query,data)
        if not result:
            return False

        result = result[0]
        book = cls(result)
        return book
    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, author, genre, cover_image, user_id) VALUES (%(title)s, %(author)s, %(genre)s, %(cover_image)s, %(user_id)s);"
        return connectToMySQL("books_galore").query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL("books_galore").query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title = %(title)s, author = %(author)s, genre = %(genre)s, cover_image = %(cover_image)s WHERE id = %(id)s;"
        return connectToMySQL("books_galore").query_db(query,data)

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

