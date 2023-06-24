from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.book import Book
bcrypt = Bcrypt(app)

@app.route("/books/<int:id>")
def view_book(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        'id': id
    }
    book = Book.get_book(data)
    return render_template("view_book.html", book = book)