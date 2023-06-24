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
        #index.html is the login page
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def create_user ():
    #Make sure the form data is valid
    #Validations should be in the model
    if not User.validate_user(request.form):
        return redirect('/')
    
    data = { 'email' : request.form['email'] }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash('Email already in use')
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    #Are we saving any other user data?
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user = User.save(data)
    session['user_id'] = user.id
    return redirect('/')

@app.route('/login', methods=['POST'] )
def login():
    data = { 'email' : request.form['email'] }
    user_in_db = User.get_by_email(data)
    #Validations for Login:
    #Email Validation
    if not user_in_db:
        print(user_in_db)
        flash("Invalid Email")
        return redirect('/')
    #Password Validation
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        print(bcrypt.generate_password_hash(request.form['password']))
        print(user_in_db.password)
        flash('Invalid Password')
        return redirect('/')
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete')
def delete():
    data = { 'id' : session['user_id'] }
    User.delete(data)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    #User must be loggin in to view the dashboard
    if not 'user_id' in session:
        return redirect('/')
    user_data = { 'id' : session['user_id']}
    user = User.get_by_id(user_data)
    #Passing in user, users, and books in case you need them
    return render_template('dashboard.html', user = user, users = User.getAll(), books = Book.getAll())

