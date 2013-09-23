import re
from error_messages import error_messages
from library import Library

def find_quoted(string):
    """returns list of substrings contained in double quotes"""
    return re.findall(r'\"(.+?)\"', string)

class LibraryTerminalInterface(object):
    def __init__(self):
        self.library = Library()
        self.commands = {}

    def run(self):
        print "Welcome to your library!"
        while True:
            user_input = raw_input('> ')
            try:
                action, args = self.parse_query(user_input)
                if action != 'quit':
                    self.execute(action, args)
                else: 
                    print 'Bye!'
                    break
            except Exception, e:
                print error_messages.get(str(e), e)

    def parse_query(self, input_string):
        """takes user input string
        returns tuple containing action and list of arguments"""
        if input_string[:4] == 'quit':
            return 'quit', []
        action, arg_string = input_string.split(" ", 1)
        sub_parser = 'parse_' + action
        args = []
        if self.has_method(sub_parser):
            exec 'args = self.' + sub_parser + '(arg_string)'
            return action, args
        else:
            raise Exception('BAD_ACTION')

    def has_method(self, name):
        """returns true if object contains method with name"""
        return name in dir(self) and callable(getattr(self, name))

    def parse_add(self, arg_string):
        """returns an ordered list containing title and author"""
        quote_terms = find_quoted(arg_string)
        if len(quote_terms) == 2:
            return quote_terms
        raise Exception('BAD_ADD_INPUT')

    def parse_show(self, arg_string):
        """returns list containing state of books to return
        and author to filter by if author supplied in arg string"""
        tokens = arg_string.split()
        args = [tokens[0]]
        if args[0] not in ['all', 'unread']:
            raise Exception('BAD_SHOW_INPUT')
        if len(tokens) > 1:
            quote_terms = find_quoted(arg_string)
            if ('by' not in arg_string) or (len(quote_terms) is not 1):
                raise Exception('BAD_SHOW_INPUT')
            author = quote_terms[0]
            args.append(author)
        return args

    def parse_read(self, arg_string):
        """returns a list containing only title
        throws exception if input string is bad"""
        quote_terms =  find_quoted(arg_string)
        if len(quote_terms) == 1:
            if len(quote_terms[0])+2 != len(arg_string):
                raise Exception('BAD_READ_INPUT')
            return quote_terms
        else:
            raise Exception('BAD_READ_INPUT')

    def execute(self, action, args):
        """executes given action with args list"""
        if action == 'add':
            self.library.add(*args)
            print 'Added "{title}" by {author}'.format(
                title = args[0],
                author = args[1])
        elif action == 'read':
            self.library.read(*args)
            print "You've read \"{title}!\"".format(title=args[0])
        elif action == 'show':
            for book in self.library.show(*args):
                print book
