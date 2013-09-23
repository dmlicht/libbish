from library import Book, Library
from ui import LibraryTerminalInterface
import pytest

@pytest.fixture
def book():
    return Book("The Grapes of Wrath", "John Steinbeck")

@pytest.fixture
def grapes(book):
    return book

@pytest.fixture
def mice():
    return Book("Of Mice and Men", "John Steinbeck")

@pytest.fixture
def moby():
    return Book("Moby Dick", "Herman Melville")

@pytest.fixture
def library():
    return Library()

@pytest.fixture
def filled_library(library, grapes, mice, moby):
    for book in [grapes, mice, moby]:
        library.add(book.title, book.author)
    return library

@pytest.fixture
def ui():
    return LibraryTerminalInterface()
