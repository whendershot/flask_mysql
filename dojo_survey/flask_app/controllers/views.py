from flask import render_template
from flask_app import app
from flask_app.db import db

@app.route('/')
def index():
    return render_template('./user_survey.html', data=db)

@app.route('/', defaults={'u_path' : ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    print(repr(u_path))
    return f'Sorry! No response. Try again. But how did you fall into here?<br>{u_path}'