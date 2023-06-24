from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book

@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, books=Book.get_all())

@app.route('/add_book/<int:id>')
def add_book(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id,
        "user_id": session['user_id']
    }
    Book.add_book(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    Book.delete(data)
    return redirect('/dashboard')


@app.route('/details/<int:id>')
def details(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    return render_template('details.html', book=Book.get_by_id(data))

@app.route('/book/edit/<int:id>')
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    return render_template('edit.html', book=Book.get_by_id(data))

@app.route('/book/update/<int:id>', methods=['POST'])
def update_book(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Book.validate_book(request.form):
        return redirect(f'/book/edit/{id}')
    data = {
        "id": id,
        "title": request.form['title'],
        "author": request.form['author'],
        "genre": request.form['genre']
    }
    Book.update_book(data)
    return redirect('/dashboard')