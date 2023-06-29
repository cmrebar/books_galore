from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request

class Review:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.book_id = data['book_id']
        self.user_id = data['user_id']
        self.book = None
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO reviews (content, book_id, user_id) VALUES (%(content)s, %(book_id)s, %(user_id)s);"
        return connectToMySQL("books_galore").query_db(query,data)
    
    @classmethod
    def delete_reviews_by_book(cls,data):
        query = "DELETE FROM reviews WHERE book_id = %(id)s;"
        return connectToMySQL("books_galore").query_db(query,data)
    
    @classmethod
    def delete_review(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL("books_galore").query_db(query,data)