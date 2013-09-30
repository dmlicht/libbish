import os
from app import app, db
from app import models
import unittest
import tempfile
import json

class TestViews(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['SQLITE_DATABASE_URL'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', app.config['SQLITE_DATABASE_URI'])
        self.test_client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        db.session.remove()

    def test_hello(self):
        """verifies basic test file configuration"""
        response = self.test_client.get('/hello')
        self.assertEqual(response.data, 'Hello World!')

    def test_create_user(self):
        self.assertEqual(models.User.query.count(), 0)
        self.test_client.post('/users?username=user1')
        self.assertEqual(models.User.query.count(), 1)

    def add_dummy_users(self, n):
        for i in xrange(n):
            self.test_client.post('/users?username=user'+str(i))

    def test_get_users(self):
        self.add_dummy_users(100)
        response = self.test_client.get('/users')
        response_dict = json.loads(response.data)
        self.assertEqual(len(response_dict['users']), 100)

    #TODO
    def test_create_user_bad_input(self):
        pass

    #TODO
    def test_create_user_username_taken(self):
        pass

    def test_create_book(self):
        self.assertEqual(models.Book.query.count(), 0)
        self.test_client.post('/books?title=thetitle&author=theauthor')
        self.assertEqual(models.Book.query.count(), 1)

    #TODO
    def test_create_book_bad_input(self):
        pass

    #TODO
    def test_create_book_taken(self):
        pass

    def add_dummy_books(self, n):
        """add n dummy books"""
        for i in xrange(n):
            self.test_client.post('/books?title=thetitle'+str(i)+'&author=theauthor'+str(i))

    def test_get_books(self):
        self.add_dummy_books(100)
        response = self.test_client.get('/books')
        response_dict = json.loads(response.data)
        self.assertEqual(len(response_dict['books']), 100)

if __name__ == "__main__":
    unittest.main()
