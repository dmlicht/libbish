Library
=======

## David Lichtenberg

## To run
./library
(may have to chmod library file to make it runnable)

## Usage
* add "<title>" "<author>"
    ** adds book with <title> and <author> to library
* read "<title>"
    ** sets state of book with <title> to read
* show <all || unread> [by "<author>"]
    ** show all books or unread books, optional selection by author
* quit

## Structure
* User input is handled in **ui.py**
* storing and retreiving the data in handled in **library.py**
* **main.py** creates an instance of TerminalLibraryInterface (from ui.py) and starts it running.

### Tests
Tests are written using the pytest framework.  
To install pytest, run: pip install pytest  
To run the tests, run: py.test  

Tests for library and ui are contained in test/test_library.py and test/test_ui.py, respectively. conftest.py contains fixture definitions.  
To learn more about pytest, visit: http://pytest.org/
