from app import db
class Book(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)

class UserBook(db.model):
    """maps many to many relationship between users and books"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    progress = db.Column()

class User(db.model):
    id = db.Column(db.Integer, db.Foreign)
    username = db.Column(db.String(80), nullable=False, unique=True)
