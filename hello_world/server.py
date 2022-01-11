from flask import Flask, render_template, request, redirect, session
import os

from friend import Friend

app = Flask(__name__.split('.')[0])
app.secret_key = os.environ.get('SESSION_SECRET_KEY')

@app.route('/')
def index():
    friends = Friend.get_all()
    print(friends)
    return render_template('index.html', all_friends=friends)

@app.route('/', defaults={'u_path' : ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    print(repr(u_path))
    return f'Sorry! No response. Try again. But how did you fall into here?<br>{u_path}'


if __name__ == '__main__':
    app.run(debug=True)