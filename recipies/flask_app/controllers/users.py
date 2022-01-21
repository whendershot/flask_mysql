from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user, recipe

bcrypt = Bcrypt(app)

@app.route('/registration')
def show_registration():

    if is_logged_in():
        return redirect('/dashboard')

    return render_template('./registration_login.html')

@app.route('/register', methods=['POST'])
def register_user():
    
    data = {
        'email' : request.form['user_email'],
        'password' : request.form['user_password'],
        'password_confirm' : request.form['user_password_confirm'],
        'first_name' : request.form['user_first_name'],
        'last_name' : request.form['user_last_name'],
    }

    #Validate form data
    if (not user.User.validate(data)):
        return redirect('/registration')

    data['password_hash'] = bcrypt.generate_password_hash(request.form['user_password'])    
    data['user_id'] = user.User.create(data)

    session['user_id'] = data['user_id']

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login_user():
    data = {
        'email' : request.form['user_email']
    }

    user_in_db = user.User.get_by_email(data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/registration')

    if not bcrypt.check_password_hash(user_in_db['password_hash'], request.form['user_password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/registration')

    session['user_id'] = user_in_db['id']

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/registration')

def is_logged_in():
    return 'user_id' in session and session['user_id'] > 0