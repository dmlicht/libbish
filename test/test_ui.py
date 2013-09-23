#David Lichtenberg
#david.m.lichtenberg@gmail.com

#definitions for fixtures (args) used in tests found in conftest.py
#for more information on fixtures: http://pytest.org/latest/fixture.html
#for general information on pytest: http://pytest.org/latest/

import pytest

def test_ui_query_add(ui, book):
    result = ui.parse_query('add "{title}" "{author}"'.format(
        title=book.title,
        author=book.author))
    assert result == ('add', [book.title, book.author])

def test_ui_parse_add_good_input(ui, book):
    good_input = '"{title}" "{author}"'.format(
        title=book.title,
        author=book.author)
    result = ui.parse_add(good_input)
    assert result == [book.title, book.author]

def test_ui_parse_add_bad_input(ui):
    bad_inputs = [
        '"too" "many" "args wrapped in double quotes"',
        '"too few args wrapped in doubles"', #too few args
        'no args wrapped in doubles'
    ]
    for bad_input in bad_inputs:
        with pytest.raises(Exception):
            ui.parse_add(bad_input)

def test_ui_parse_read(ui, book):
    good_input = '"{title}"'.format(title = book.title)
    assert ui.parse_read(good_input) == [book.title]

def test_ui_parse_read_bad_input(ui):
    bad_inputs = [
        'title not wrapped in double quotes',
        '"title" with extra data outside of double quotes',
        '"too many" "things wrapped in doubles"'
    ]
    for bad_input in bad_inputs:
        with pytest.raises(Exception):
            ui.parse_read(bad_input)

def test_ui_parse_show_all(ui):
    good_input = 'all'
    assert ui.parse_show(good_input) == ['all']

def test_ui_parse_show_all_by_author(ui, book):
    good_input = 'all by "{author}"'.format(author=book.author)
    assert ui.parse_show(good_input) == ['all', book.author]

def test_ui_parse_show_unread(ui, book):
    good_input = 'unread'
    assert ui.parse_show(good_input) == ['unread']

def test_ui_parse_show_unread_by_author(ui, book):
    good_input = 'unread by "{author}"'.format(author=book.author)
    assert ui.parse_show(good_input) == ['unread', book.author]

def test_ui_parse_show_bad_input(ui):
    bad_input = 'bad_input'
    with pytest.raises(Exception):
        ui.parse_show(bad_input)

def test_ui_execute_add(ui, book):
    ui.execute('add', [book.title, book.author])
    assert book in ui.library.books

def test_ui_execute_add_string(ui, book, capsys): #capsys allows us to look to writes for standard output
    ui.execute('add', [book.title, book.author])
    expected =  'Added "{title}" by {author}\n'.format(
            title=book.title, 
            author=book.author)
    result = capsys.readouterr()[0]
    assert expected == result

def test_ui_execute_read(ui, book):
    ui.library.add_instance(book)
    ui.execute('read', [book.title])
    assert ui.library.books[0].read

def test_ui_read_string(ui, book, capsys):
    ui.library.add_instance(book)
    ui.execute('read', [book.title])
    expected = "You've read \"{title}!\"\n".format(title=book.title)
    result = capsys.readouterr()[0]
    assert expected == result

def test_ui_execute_show(ui, filled_library, capsys):
    ui.library = filled_library
    ui.execute('show', ['all'])
    expected = '"The Grapes of Wrath" by John Steinbeck (unread)\n"Of Mice and Men" by John Steinbeck (unread)\n"Moby Dick" by Herman Melville (unread)\n'
    result = capsys.readouterr()[0]
    assert expected == result
