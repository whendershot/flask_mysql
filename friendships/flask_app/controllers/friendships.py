from flask_app import app
from flask import render_template, request, redirect, jsonify
from flask_app.models import friendship, user

@app.route('/friendships')
def show_friendships():
    _friendships = friendship.Friendship.get_all()
    _users = user.User.get_all()
    _potential_friends = friendship.Friendship.get_potential_friends({'user_id': _users[0]['id']})
    return render_template('friendships.html', friendships=_friendships, users=_users, potential_friends=_potential_friends)

@app.route('/friendships/_get_potential/')
def get_potential_friends():
    
    _selected_user = request.args.get('selected_user')
    _selected_potential_friends = friendship.Friendship.get_potential_friends({'user_id': _selected_user})
    html_string = ""
    for user in _selected_potential_friends:
        html_string += f'<option value="{user["id"]}">{user["first_name"]} {user["last_name"]}</option>'
    return jsonify(html_string=html_string)

@app.route('/friendships/create', methods=['POST'])
def create_friendship():
    data = {
        'user_id' : request.form.get('user_id'),
        'friend_id' : request.form.get('friend_id')
    }
    result = friendship.Friendship.create(data)
    return redirect('/friendships')