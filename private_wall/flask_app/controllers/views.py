from flask_app import app
from flask import redirect
from babel.dates import format_datetime

@app.route('/')
def show_index():
    return redirect('/registration')

@app.route('/', defaults={'u_path' : ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    print(repr(u_path))
    return f'Sorry! No response. Try again. But how did you fall into here?<br>{u_path}'

@app.template_filter('format_datetime')
def _format_datetime(value, format="MMMM d, yyyy"):
    return format_datetime(value, format)