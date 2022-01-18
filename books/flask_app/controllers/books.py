from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import book, author, favoriteBook

@app.route('/books')
def show_books():
    books = book.Book.get_all()
    return render_template('books.html', books=books)

@app.route('/books/create', methods=['POST'])
def create_book():
    data = {
        'title' : request.form.get('title'),
        'num_of_pages' : request.form.get('num_of_pages')
    }
    result = book.Book.create(data)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):
    data = {
        'book_id' : id
    }
    _book = book.Book.get_by_id(data)
    _authors = author.Author.get_all()
    _favorites = favoriteBook.FavoriteBook.get_all_authors(data)
    print(_book)
    return render_template('book.html', book=_book, authors=_authors, favorites=_favorites)