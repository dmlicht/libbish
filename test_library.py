#David Lichtenberg
#david.m.lichtenberg@gmail.com

#definitions for fixtures (args) used in tests found in conftest.py
#for more information on fixtures: http://pytest.org/latest/fixture.html
#for general information on pytest: http://pytest.org/latest/

import app
import unittest
from app.models import Book, UserBook, User, empty_and_whitespace_to_none
from app import db

class TestHelpers(unittest.TestCase):
    def test_convert_bad_strings_to_none(self):
        input = ["one", "two", "", "    ", "five"]
        expected = ["one", "two", None, None, "five"]
        result = empty_and_whitespace_to_none(*input)
        self.assertEqual(expected, result)

    def test_convert_bad_strings_to_none_single_input(self):
        input = "one"
        expected = "one"
        result = empty_and_whitespace_to_none(input)
        self.assertEqual(expected, result)

class DBTestCase(unittest.TestCase):
    def create_should_fail_with(self, model, *args, **kwargs):
        """tries to add instance to model.
        check to make sure it fails, then rollsback to past state"""
        with self.assertRaises(Exception):
            app.db.session.add(model(*args, **kwargs))
            app.db.session.commit()
        app.db.session.rollback()

    def create_should_succeed_with(self, model, *args, **kwargs):
        """tries to add instance to model.
        checks for success, KEEPS added element in database"""
        start_count = model.query.count()
        new_instance = model(*args, **kwargs)
        app.db.session.add(new_instance)
        app.db.session.commit()
        self.assertEqual(model.query.count(), start_count + 1)

    def setUp(self):
        app.db.create_all()

    def tearDown(self):
        app.db.drop_all()
        app.db.session.remove()


class TestBook(DBTestCase):
    def test_book_instantiation(self):
        new_book = Book("the title", "the author")
        self.assertTrue(new_book)

    def test_book_creation_adds_book_to_db(self):
        self.create_should_succeed_with(Book, "the title", "the author")

    def test_two_books_can_have_same_title_diff_author(self):
        same_title = "the title"
        self.create_should_succeed_with(Book, same_title, "author")
        self.create_should_succeed_with(Book, same_title, "different author")

    def test_two_books_can_have_same_author_diff_title(self):
        same_author = "the author"
        self.create_should_succeed_with(Book, "title", same_author)
        self.create_should_succeed_with(Book, "diff title", same_author)

    def test_book_cannot_create_without_title(self):
        self.create_should_fail_with(Book, author="my author")

    def test_book_cannot_create_without_author(self):
        self.create_should_fail_with(Book, title="my title")

    def test_book_cannot_create_space_title(self):
        self.create_should_fail_with(Book, title="    ", author="my author")

    def test_book_cannot_create_space_author(self):
        self.create_should_fail_with(Book, title="my title", author="     ")

    def test_book_cannot_create_empty_title(self):
        self.create_should_fail_with(Book, title="", author="my author")

    def test_book_cannot_create_empty_author(self):
        self.create_should_fail_with(Book, title="my title", author="")

    def test_book_creation_two_books_same_info(self):
        app.db.session.add(Book("the title", "the author"))
        app.db.session.commit()
        self.create_should_fail_with(Book, title="the title", author="the author")
        self.assertEqual(Book.query.count(), 1)


class TestUser(DBTestCase):
    def test_create_user(self):
        self.create_should_succeed_with(User, "my_username")

    def test_create_multiple_users_different_names(self):
        names = ["david", "mike", "greg", "al"]
        for name in names:
            self.create_should_succeed_with(User, name)

    def test_cannot_create_with_same_name(self):
        self.create_should_succeed_with(User, "greg")
        self.create_should_fail_with(User, "greg")

    def test_cannot_create_user_empty_username(self):
        self.create_should_fail_with(User, "")

    def test_cannot_create_user_whitespace_username(self):
        self.create_should_fail_with(User, "    ")

if __name__ == '__main__':
    unittest.main()
