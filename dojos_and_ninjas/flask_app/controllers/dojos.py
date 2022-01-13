from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja


@app.route('/dojos')
def show_dojos():
    dojos = Dojo.get_all()
    return render_template('dojos.html', dojos=dojos)

@app.route('/dojos/create', methods=['POST'])
def create_dojo():
    data = {
        'name' : request.form.get('dojo_name')
    }
    result = Dojo.create(data)
    return redirect('/dojos')

@app.route('/dojos/<int:id>')
def show_dojo(id):
    data = {
        'dojo_id' : id
    }
    dojo = Dojo.get_one(data)
    ninjas = Ninja.get_all_by_dojo_id(id)
    print(dojo)
    return render_template('dojos_show_one.html', dojo=dojo, ninjas=ninjas)