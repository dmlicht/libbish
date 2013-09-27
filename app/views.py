from app import app, db
from app.models import User, Book, UserBook
from flask import render_template, request, redirect, url_for, session, jsonify

@app.route('/hello')
def hello():
    return 'Hello World!'

@app.route('/books', methods = ['GET', 'POST'])
def book_index():
    if request.method == "GET":
        query = Book.query.all()
        return jsonify({'books': [book.to_dict() for book in query]})

    if request.method == "POST":
        if request.args['title'] and request.args['author']:
            db.session.add(Book(request.args['title'], request.args['author']))
            db.session.commit()
        else:
            pass #TODO: handle bad params
        return 'OK'

@app.route('/users', methods=['GET', 'POST'])
def user_index():
    if request.method == "GET":
        query = User.query.all()
        return jsonify({'users': [user.to_dict() for user in query]})
    if request.method == "POST":
        if request.args['username']:
            db.session.add(User(request.args['username']))
            db.session.commit()
        else:
            pass #TODO: handle bad params
        return 'OK'

@app.route('/users/<id>', methods=['GET', 'POST'])
def user_books(id):
    """user can display and add books"""
    user = User.query.get(id)
    if not user:
        return "ERROR" #TODO: add real error handling
    if request.method == 'GET':
        pass
        user_dict = user.to_dict()
        books = {}
        books['in_progress'] = [book_assoc.book.to_dict() for book_assoc in user.book_assocs if book_assoc.state == "in progress"]
        books['unread'] = [book_assoc.book.to_dict() for book_assoc in user.book_assocs if book_assoc.state == "unread"]
        books['read'] = [book_assoc.book.to_dict() for book_assoc in user.book_assocs if book_assoc.state == "read"]
        user_dict['books'] = books
        return jsonify(user_dict)
    if request.method == 'POST':
        if request.args['book_id']:
            book = Book.query.get(id)
            user.add(book)
            db.session.commit()
            return 'OK'
