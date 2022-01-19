from flask import render_template, request, redirect, session
from flask_app.controllers import views, dojoSurveys
from flask_app import app


if __name__ == '__main__':
    app.run(debug=True)