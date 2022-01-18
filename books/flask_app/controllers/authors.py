from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import book, author, favoriteBook

@app.route('/authors')
def show_authors():
    _authors = author.Author.get_all()
    print(_authors)
    return render_template('authors.html', authors=_authors)

@app.route('/authors/create', methods=['POST'])
def create_author():
    data = {
        'author_name' : request.form.get('author_name')
    }
    result = author.Author.create(data)
    return redirect('/authors')

@app.route('/authors/<int:id>')
def show_author(id):
    data = {
        'author_id' : id
    }
    _author = author.Author.get_by_id(data)
    _books = book.Book.get_potential_books(data)
    _favorites = favoriteBook.FavoriteBook.get_all_books(data)
    return render_template('author.html', author=_author, books=_books, favorites=_favorites)