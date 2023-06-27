from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.book import Book

#View a book
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

#Add book page
@app.route("/books/add")
def add_book():
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    return render_template("create_book.html")

#Save book
@app.route("/books/save", methods=['POST'])
def save_book():
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    #Make sure the form data is valid
    #Validations should be in the model
    if not Book.validate_book(request.form):
        return redirect('/books/add')
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'cover_image': request.files['cover_image'],
        'review': request.form['review'],
        'user_id': session['user_id']
    }
    Book.save(data)
    return redirect("/dashboard")

#Edit book page
@app.route("/books/<int:id>/edit")
def edit_book(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        'id': id
    }
    book = Book.get_book(data)
    return render_template("edit_book.html", book = book)

#Update book
@app.route("/books/<int:id>/update", methods=['POST'])
def update_book(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    #Make sure the form data is valid
    #Validations should be in the model
    if not Book.validate_book(request.form):
        return redirect(f"/books/{id}/edit")
    data = {
        'id': id,
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'cover_image': request.files['cover_image'],
        'review': request.form['review']
    }
    Book.update_book(data)
    return redirect("/dashboard")

#Delete book
@app.route("/books/<int:id>/delete")
def delete_book(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        'id': id
    }
    Book.delete_book(data)
    return redirect("/dashboard")

