from flask_app import app
from flask_app.controllers import users

@app.route('/', defaults={'u_path' : ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    print(repr(u_path))
    return f'Sorry! No response. Try again. But how did you fall into here?<br>{u_path}'

if __name__ == '__main__':
    app.run(debug=True)