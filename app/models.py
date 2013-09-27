from app import db

def empty_and_whitespace_to_none(*strings):
    """replaces empty strings and all whitespace strings with None objects"""
    def is_okay(string):
        return not (string.isspace() or string == "")
    checked = [string if is_okay(string) else None for string in strings]
    return checked if len(checked) > 1 else checked[0] 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    __table_args__ = (db.UniqueConstraint('title', 'author', name='title_author_unique'),)

    def __init__(self, title, author):
        title, author = empty_and_whitespace_to_none(title, author)
        self.title = title
        self.author = author

class UserBook(db.Model):
    """maps many to many relationship between users and books"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    #NOTE: REMEMBER TO SET CONSTRAINTS WHEN YOU HAVE INTERNET
    progress = db.Column(db.String(80)) 

    #user = db.relationship("User", backref="user_books")
    #book = db.relationship("Book", backref="user_books")

    def __init__(self):
        self.progress = "UNREAD"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, username):
        username = empty_and_whitespace_to_none(username)
        self.username = username
