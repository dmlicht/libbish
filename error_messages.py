error_messages = {
    'BAD_ACTION': "error with first term in query - please user add, read, show, or quit",
    'BAD_ADD_INPUT': """
    error with input supplied for add statement, please format:
    add "<title>" "<author>"
    where <title> and <author> correspond to book info
    example: add "The Grapes of Wrath" "John Steinbeck"
    """,
    'BAD_READ_INPUT': """
    error with input supplied for read statement, please format:
    read "<title>"
    where <title> corresponds to book to read
    """,
    'BAD_SHOW_INPUT': """
    error with input supplied for show statement, please format:
    show <all || unread> [by <author>]
    where user chooses between all and unread and by author is optional
    example: show unread by "John Steinbeck"
    example: show all
    """,
    'SAME_TITLE': """
    A book with this title already exists so we can't add it. Sorry :(
    """,
    'NO_BOOK': """
    This book isn't in your library. To see which books you own, try typing:
    show all
    """
}
