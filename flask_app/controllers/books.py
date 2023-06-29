from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.book import Book
from flask_app.models.review import Review
#View a book
@app.route("/books/<int:id>")
def view_book(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        'id': id
    }
    book = Book.get_book_with_reviews(data)
    user = User.get_by_id({'id': session['user_id']})
    return render_template("view_book.html", book = book, user = user)

#Add book page
@app.route('/books/add')
def add_book():
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template("add_book.html", user = user)

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
    
    image = request.files['cover_image']
    image.save('flask_app/static/images/' + image.filename)
    image_url = '/static/images/' + image.filename
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'cover_image': image_url,
        'review': request.form['review'],
        'user_id': session['user_id']
    }
    Book.save(data)
    data = {
        'title': request.form['title']
    }
    book = Book.get_by_title(data)
    data = {
        'content': request.form['review'],
        'user_id': session['user_id'], 
        'book_id': book.id

    }
    Review.save(data)
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
    book = Book.get_by_id(data)
    user = User.get_by_id({'id': session['user_id']})
    return render_template("edit_book.html", book = book, user = user)

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
    image = request.files['cover_image']
    image.save('flask_app/static/images/' + image.filename)
    image_url = '/static/images/' + image.filename
    data = {
        'id': id,
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'cover_image': image_url
    }
    Book.update(data)
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
    Review.delete_reviews_by_book(data)
    Book.delete(data)
    return redirect("/dashboard")

@app.route("/books/<int:id>/review", methods=['POST'])
def review_book(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        'content': request.form['review'],
        'user_id': session['user_id'], 
        'book_id': id

    }
    Review.save(data)
    return redirect(f"/books/{id}")

@app.route("/books/<int:id>/delete_review")
def delete_review(id):
    if not 'user_id' in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        'id': id
    }
    Review.delete_review(data)
    return redirect("/dashboard")
