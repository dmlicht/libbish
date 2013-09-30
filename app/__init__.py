from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import *

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

def init_db():
    db.create_all()
init_db()

from app import views
