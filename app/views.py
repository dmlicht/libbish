from app import app, db
from app.models import User, Book, UserBook
from flask import render_template, request, redirect, url_for, session, jsonify
from helpers import filter_factory

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/books', methods=['GET', ])
def get_books():
    query = Book.query.all()
    return jsonify({'books': [book.to_dict() for book in query]})

@app.route('/books', methods=['POST', ])
def post_book():
    if request.form['title'] and request.form['author']:
        db.session.add(Book(request.form['title'], request.form['author']))
        db.session.commit()
    else:
        return "UNIMPLEMENTED ERROR HANDLING"
    return 'OK'

@app.route('/books/<int:book_id>', methods=['GET', ])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'book':book.to_dict()})
    else:
        return "UNIMPLEMENTED ERROR HANDLING"

@app.route('/users', methods=['GET', ])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]})

@app.route('/users', methods=['POST', ])
def post_user():
    if request.form['username']:
        db.session.add(User(request.form['username']))
        db.session.commit()
        return "OK"
    else:
        return "UMIMPLEMENTED ERROR HANDLING"

@app.route('/users/<int:user_id>', methods=['GET', ])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify({'user': user.to_dict()})

@app.route('/users/<int:user_id>/books', methods=['GET', ])
def get_user_books(user_id):
    user = User.query.get(user_id)
    if not user:
        return "UNIMPLEMENTED ERROR HANDLING"
    my_filter = filter_factory(request.args['read_state'], 'state')
    books_dicts = [assoc.book for assoc in user.book_assocs if my_filter(assoc)]
    return jsonify({'books': books_dicts})

@app.route('/users/<int:user_id>/books/<int:book_id>', methods=['PUT'])
def put_user_book(user_id, book_id):
    pass

@app.route('/users/<int:user_id>/books', methods=['POST', ])
def post_user_book(user_id):
    user = User.query.get(user_id)
    if request.form['book_id'] and user:
        book = Book.query.get(int(request.form['book_id']))
        user.add(book)
        db.session.commit()
        return 'OK'
    else:
        return 'ADD ERROR HANDLING'
