from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.user import User
from babel.dates import format_datetime

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def display_users():
    users = User.get_all()
    return render_template('users.html', all_users=users)

@app.route('/users/new')
def new_user():
    return render_template('users_new.html')

@app.route('/users/create', methods=['POST'])
def create_user():
    data = {
        'first_name' : request.form.get('first_name'),
        'last_name' : request.form.get('last_name'),
        'email' : request.form.get('email'),
    }
    User.create(data)
    return redirect("/users")

@app.template_filter('format_datetime')
def _format_datetime(value, format="MMMM d, yyyy"):
    return format_datetime(value, format)