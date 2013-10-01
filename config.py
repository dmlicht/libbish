import os

_basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('DATABASE_URL') is None:
    SQLITE_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLITE_DATABASE_URI)
DEBUG = True
