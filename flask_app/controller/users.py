from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('login.html')

@app.route('/login/process', methods=['POST'])
def logged_in():
    user = User.validate_login(request.form)
    if not user:
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/register/process', methods=['POST'])
def registered():
    if not User.validate_reg(request.form):
        return redirect('/')

    user_id = User.save(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')