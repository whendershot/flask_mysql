from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.friend import Friend

@app.route('/')
def index():
    return redirect("/friends")

@app.route('/friends')
def display_friends():
    friends = Friend.get_all()
    print(friends)
    return render_template('friends.html', all_friends=friends)

@app.route('/create/friend', methods=['POST'])
def create_friend():
    data = {
        "first_name" : request.form.get("fname"),
        "last_name" : request.form.get("lname"),
        "occupation" : request.form.get("occ")
    }
    Friend.add_friend(data)
    return redirect("/friends")