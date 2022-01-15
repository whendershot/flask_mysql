from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import book, author

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