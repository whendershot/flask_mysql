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

@app.route('/users/<int:id>')
def show_user(id):
    data = {
        'user_id' : id
    }
    user = User.get_user(data)
    return render_template('users_show.html', user=user)

@app.route('/users/new')
def new_user():
    return render_template('users_new.html')

@app.route('/users/<int:id>/edit')
def editing_user(id):
    data = {
        'user_id' : id
    }
    user = User.get_user(data)
    return render_template('users_edit.html', user=user)

@app.route('/users/<int:id>/update', methods=['POST'])
def update_user(id):
    data = {
        'user_id' : id,
        'first_name' : request.form.get('first_name'),
        'last_name' : request.form.get('last_name'),
        'email' : request.form.get('email')
    }
    print(f'Updating user id: {id}')
    print(data)
    result = User.update_user(data)
    print(result)
    return redirect('/users/' + str(id))

@app.route('/users/<int:id>/destroy')
def destroy_user(id):
    data = {
        'id' : id
    }
    result = User.destroy(data)
    print(result)
    return redirect('/users')

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