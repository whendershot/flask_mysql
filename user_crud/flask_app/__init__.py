from flask import Flask
import os

app = Flask(__name__.split('.')[0])
app.secret_key = os.environ.get('SESSION_SECRET_KEY')