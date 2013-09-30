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
    if request.args['title'] and request.args['author']:
        db.session.add(Book(request.args['title'], request.args['author']))
        db.session.commit()
    else:
        return "UNIMPLEMENTED ERROR HANDLING"
    return 'OK'

@app.route('/books/<int:id>', methods=['GET', ])
def get_book():
    book = Book.query.get(id)
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
    if request.args['username']:
        db.session.add(User(request.args['username']))
        db.session.commit()
        return "OK"
    else:
        return "UMIMPLEMENTED ERROR HANDLING"

@app.route('/users/<int:id>', methods=['GET', ])
def get_user(id):
    user = User.query.get(id)
    return jsonify({'user': user.to_dict()})

@app.route('/users/<int:id>/books', methods=['GET', ])
def get_user_books(id):
    user = User.query.get(id)
    if not user:
        return "UNIMPLEMENTED ERROR HANDLING"
    my_filter = filter_factory(request.args['read_state'], 'state')
    books_dicts = [assoc.book for assoc in user.book_assocs if my_filter(assoc)]
    return jsonify({'books': books_dicts})

@app.route('/users/<int:id>/books', methods=['POST', ])
def post_user_book(id):
    user = User.query.get(id)
    if request.args['book_id'] and user:
        book = Book.query.get(int(request.args['book_id']))
        user.add(book)
        db.session.commit()
        return 'OK'
    else:
        return 'ADD ERROR HANDLING'
