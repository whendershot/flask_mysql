from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import book, author

@app.route('/authors')
def show_authors():
    authors = author.Author.get_all()
    return render_template('authors.html', authors=authors)

@app.route('/authors/create', methods=['POST'])
def create_author():
    data = {
        'name' : request.form.get('name')
    }
    result = author.Author.create(data)
    return redirect('/authors')