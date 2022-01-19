from flask_app import app
from flask_app.controllers import views, emails

if __name__ == '__main__':
    app.run(debug=True)