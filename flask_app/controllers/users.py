from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.book import Book
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if not 'user_id' in session:
        flash('You must login to continue')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def create_user ():
    #Make sure the form data is valid
    #Validations should be in the model
    if not User.validate_reg(request.form):
        return redirect('/')
    #Make sure the email is not already in use
    data = { 'email' : request.form['email'] }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash('Email already in use')
        return redirect('/')
    #Hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    #Are we saving any other user data?
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user = User.save(data)
    return redirect('/')

@app.route('/login', methods=['POST'] )
def login():
    data = { 'email' : request.form['email'] }
    user_in_db = User.get_by_email(data)
    #Validations for Login:
    #Email Validation
    if not user_in_db:
        flash("Invalid Email")
        return redirect('/')
    #Password Validation
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Password')
        return redirect('/')
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

#Logout User
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#Delete User
@app.route('/delete')
def delete():
    data = { 'id' : session['user_id'] }
    User.delete(data)
    return redirect('/')

#Dashboard
@app.route('/dashboard')
def dashboard():
    #User must be logged in to view the dashboard
    if not 'user_id' in session:
        return redirect('/')
    #Get the user from the database
    data = { 'id' : session['user_id']}
    user = User.get_by_id(data)
    #Passing in user, users, and books in case you need them
    return render_template('index.html', user = user, users = User.getAll(), books = Book.getAll())

