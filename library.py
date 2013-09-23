class Book(object):
    """groups title, author and read state and make printing easier"""
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.read = False

    def __str__(self):
        """returns string representation of book"""
        state = '(read)' if self.read else '(unread)'
        return '"{title}" by {author} {state}'.format(
            title = self.title,
            author = self.author,
            state = state
        )

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class Library(object):
    def __init__(self):
        self.books = []
        self.by_title = {} #for faster .read calls
        self.by_author = {} #for faster by author lookups (dictionary of lists)

    def add(self, title, author):
        """stores book with given title and author in library"""
        new_book = Book(title, author)
        self.add_instance(new_book)

    def add_instance(self, book):
        """stores passed book instance in retrieval data structures"""
        if self.by_title.get(book.title, False): #NOTE assuming that we cannot add two books with the same title
            raise Exception('SAME_TITLE')
        self.books.append(book)
        self.by_title[book.title] = book
        self.by_author[book.author] = self.by_author.get(book.author, [])
        self.by_author[book.author].append(book)

    def read(self, title):
        """looks up a book given its title and changes its read state to true
        bad input is currently just ignored"""
        book = self.by_title.get(title, False)
        if book:
            book.read = True
        else:
            raise Exception('NO_BOOK')

    def show(self, all_or_unread, author=None):
        """takes a list of filters and returns the subset of books that matches
        if no books associated with author, no books will be returned"""
        if author:
            books = self.by_author.get(author, [])[:] #[:] creates copy instead of ref
        else:
            books = self.books[:]
        if all_or_unread == 'unread':
            books = [book for book in books if not book.read]
        return books
