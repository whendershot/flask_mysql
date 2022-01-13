from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

@app.route('/ninjas/')
def new_ninja():
    dojos = Dojo.get_all()
    return render_template('ninjas_create.html', dojos=dojos)

@app.route('/ninjas/create', methods=['POST'])
def create_ninja():
    data = {
        'dojo_id' : request.form.get('dojo_id'),
        'first_name' : request.form.get('first_name'),
        'last_name' : request.form.get('last_name'),
        'age' : request.form.get('age')
    }
    result = Ninja.create(data)
    return redirect('/dojos/' + str(data['dojo_id']))