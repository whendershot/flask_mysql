from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user, programmingLanguages

bcrypt = Bcrypt(app)

@app.route('/users')
def show_registration():

    if not is_logged_in:
        return redirect('/dashboard')

    _p_languages = programmingLanguages.ProgrammingLanguages.get_all()
    return render_template('./registration_login.html', p_languages=_p_languages)

@app.route('/register', methods=['POST'])
def register_user():
    
    print(f'Registration form: {request.form}')

    data = {
        'email' : request.form['user_email'],
        'password' : request.form['user_password'],
        'password_confirm' : request.form['user_password_confirm'],
        'first_name' : request.form['user_first_name'],
        'last_name' : request.form['user_last_name'],
        'birthday' : request.form['user_birthday'],
        'age' : request.form['user_age'],
        'p_languages' : request.form.getlist('user_p_languages')
    }

    print(f'Initial data block: {data}')
    #Validate form data
    if (not user.User.validate(data)):
        return redirect('/users')

    if (not user.UserPII.validate(data)):
        return redirect('/users')

    data['email_hash'] = bcrypt.generate_password_hash(request.form['user_email'])
    data['password_hash'] = bcrypt.generate_password_hash(request.form['user_password'])
    
    data['user_id'] = user.User.create(data)
    _user_pii_id = user.UserPII.create(data)

    print(f'Langs: {data["p_languages"]}')
    if (data['p_languages'] and len(data['p_languages']) > 0):
        for i in data['p_languages']:            
            programmingLanguages.LanguagesUsed.create({
                'user_id': data['user_id'],
                'programming_language_id' : i
                })

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
        return redirect('/users')

    if not bcrypt.check_password_hash(user_in_db.password_hash, request.form['user_password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/users')

    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return redirect('/users')

@app.route('/dashboard')
def logged_in():
    
    if not is_logged_in():
        return redirect('/users')

    data = {
        'user_id' : session['user_id']
    }

    data['user'] = user.UserPII.get_one(data)
    data['langs'] = programmingLanguages.LanguagesUsed.get_by_user(data)
    return render_template('./success.html', data=data)


def is_logged_in():
    return 'user_id' in session and session['user_id'] > 0