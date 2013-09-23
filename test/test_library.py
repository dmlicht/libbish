#David Lichtenberg
#david.m.lichtenberg@gmail.com

#definitions for fixtures (args) used in tests found in conftest.py
#for more information on fixtures: http://pytest.org/latest/fixture.html
#for general information on pytest: http://pytest.org/latest/

from library import Book

def test_create_book(book):
    assert book

def test_book_str(book):
    expected = '"The Grapes of Wrath" by John Steinbeck (unread)'
    result = str(book)
    assert expected == result

def test_library(library):
    assert library

def test_add_book_to_library(library, book):
    library.add(book.title, book.author)
    book_in_lib = library.books[0]
    assert book_in_lib.title == book.title
    assert book_in_lib.author == book.author
    assert book_in_lib.read is not True

def test_book_equality(library, book):
    some_other_book = Book("other_title", "other_author")
    library.add(book.title, book.author)
    book_in_lib = library.books[0]
    assert book_in_lib == book
    assert not (book_in_lib == some_other_book)

def test_add_instance(library, book):
    library.add_instance(book)
    assert book in library.books

def test_show_all(filled_library, grapes, mice, moby):
    shown = filled_library.show('all')
    for book in [grapes, mice, moby]:
        assert book in shown

def test_show_unread_contains_all_unread(filled_library, grapes, mice, moby):
    filled_library.read(grapes.title)
    shown = filled_library.show('unread')
    for book in [mice, moby]:
        assert book in shown

def test_show_unread_does_not_contain_read(filled_library, grapes, mice, moby):
    reading_list = [grapes, mice]
    for book in reading_list:
        filled_library.read(book.title)
    shown = filled_library.show('unread')
    for book in reading_list:
        assert not (book in shown)

def test_show_all_by_author(filled_library, grapes, mice, moby):
    steinbooks = [grapes, mice]
    shown = filled_library.show('all', grapes.author)
    for book in steinbooks:
        assert book in shown
    assert not (moby in shown)
