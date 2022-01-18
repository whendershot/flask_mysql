from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import user

@app.route('/users/create', methods=['POST'])
def create_user():
    data = {
        'first_name' : request.form.get('user_first_name'),
        'last_name' : request.form.get('user_last_name')
    }
    result = user.User.create(data)
    return redirect('/friendships')