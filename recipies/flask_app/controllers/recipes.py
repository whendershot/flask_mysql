from flask_app import app
from flask import render_template, session, request, redirect
from flask_app.models import user, recipe

@app.template_filter('format_is_under_30_minutes')
def _format_is_under_30_minutes(value):
    return 'yes' if value else 'no'

@app.route('/recipes/new')
def new_recipe():

    return render_template('/create_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():

    print(f'Request form: {request.form}')

    data = {
        'user_id' : session['user_id'],
        'name' : request.form['recipe_name'],
        'description' : request.form['recipe_description'],
        'instructions' : request.form['recipe_instructions'],
        'is_under_30_minutes' : 'recipe_is_under_30_minutes' in request.form,
        'made_on' : request.form['recipe_made_on']
    }

    print(f'Recipe form: {data}')

    #Validate form data
    if (not recipe.Recipe.validate(data)):
        return redirect('/recipes/new')

    result = recipe.Recipe.create(data)

    return redirect('/dashboard')

@app.route('/dashboard')
def logged_in():
    
    if not is_logged_in():
        return redirect('/registration')

    data = {
        'user_id' : session['user_id']
    }

    data['user'] = user.User.get_one({'id':data['user_id']})
    data['recipes'] = recipe.Recipe.get_all()
    return render_template('./dashboard.html', data=data)


@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    
    data = {
        'recipe' : recipe.Recipe.get_one({'id' : recipe_id})
    }
    return render_template('edit_recipe.html', data=data)

@app.route('/recipes/edit/<int:recipe_id>/', methods=['POST'])
def make_edit_recipe(recipe_id):

    data = {
        'id' : request.form['recipe_id'],
        'name' : request.form['recipe_name'],
        'description' : request.form['recipe_description'],
        'instructions' : request.form['recipe_instructions'],
        'is_under_30_minutes' : 'recipe_is_under_30_minutes' in request.form,
        'made_on' : request.form['recipe_made_on']
    }

    #Validate form data
    if (not recipe.Recipe.validate(data)):
        return redirect(f'/recipes/edit/{recipe_id}')

    result = recipe.Recipe.update(data)

    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):

    data = {
        'user' : user.User.get_one({'id' : session['user_id']}),
        'recipe' : recipe.Recipe.get_one({'id' : recipe_id})
    }
    return render_template('show_recipe.html', data=data)

def is_logged_in():
    return 'user_id' in session and session['user_id'] > 0

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):

    data = {
        'user_id' : session['user_id'],
        'recipe_id' : recipe_id
    }

    if recipe.Recipe.is_owner(data):
        result = recipe.Recipe.delete({'id' : recipe_id})

    return redirect('/dashboard')