from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import book, author, favoriteBook

@app.route('/favorites/create', methods=['POST'])
def create_favoriteBook():
    data = {
        'author_id' : request.form.get('author_id'),
        'book_id' : request.form.get('book_id')
    }
    return_url = request.form.get('return_url')
    result = favoriteBook.FavoriteBook.create(data)
    return redirect(return_url)