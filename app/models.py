from app import db
from sqlalchemy.ext.associationproxy import association_proxy

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
    users = association_proxy('user_assocs', 'user')

    def __init__(self, title, author):
        title, author = empty_and_whitespace_to_none(title, author)
        self.title = title
        self.author = author

    def to_dict(self):
        """returns dictionary representation of Book without database members"""
        return {'id': self.id, 'title': self.title, 'author': self.author}

class UserBook(db.Model):
    """maps many to many relationship between users and books"""
    __tablename__ = 'user_book'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    #TODO: set constraints on progress values
    progress = db.Column(db.String(80)) #unread, in progress, read

    user = db.relationship("User", backref="book_assocs")
    book = db.relationship("Book", backref="user_assocs")

    def __init__(self, user, book, progress="UNREAD"):
        self.progress = progress
        self.user = user
        self.book = book

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    books = association_proxy('book_assocs', 'book')

    def create_and_add(self, title, author):
        """creates a book and associates it with a user
        checks too see if book with title and author exist. if so it just adds that book"""
        book = Book.query.filter_by(title=title, author=author).first()
        self.add(book or Book(title, author))

    def add(self, book):
        """associates book with user"""
        assoc = UserBook(self, book)
        self.book_assocs.append(assoc)

    def __init__(self, username):
        username = empty_and_whitespace_to_none(username)
        self.username = username

    def to_dict(self):
        """returns dictionary representation of User without database members"""
        return {'id': self.id, 'username': self.username}
