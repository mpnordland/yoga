from yoga import ArgumentParser
from collections import namedtuple

params_holder = namedtuple("params_holder", ['options', 'positionals'])

class ParseFunc(object):
    """
    Class to store parser and func to be called later

    This class allows each decorated function to be used repeatedly without
    rebuilding the parser
    """
    def __init__(self, func, parser):
        """
        Setup the object

        param: func - the decorated function
        param: parser - the parser built by _make_parser
        """
        self.func = func
        self.parser = parser

    def __call__(self, args):
        """
        Call the function with the parsed arguments

        param: args - the unparsed argument string
        """
        return self.func(**self.parser.parse(args))


class ParseMethod(ParseFunc):
    """
    Subclass of ParseFunc that works for methods

    Defines or overides methods that make ParseFunc work for methods
    """
    def __call__(self, f_self, args):
        """
        Call the function with the parsed arguments

        param: f_self - Self for the instance the method is set on
        param: args - the unparsed argument string
        """
        return self.func(f_self, **self.parser.parse(args))

    def __get__(self, obj, objtype):
        """
        Support instance methods.

        We need this so the decorated method's self attribute is passed
        correctly. Uses functools to bind the instance passed in when the
        method is __get__'ed to the __call__ method of this instance

        param: obj - the instance the decorated method is bound to
        param: objtype - the type of obj
        """
        import functools
        return functools.partial(self.__call__, obj)

def _get_params(func):
    """
    Get the params for the function being decorated

    Ensures the __yoga_params__ attribute is set and then returns it

    param: func - The function being decorated
    """
    if not hasattr(func, "__yoga_params__"):

        func.__yoga_params__ = params_holder([], [])
    return func.__yoga_params__

def _make_parser(func):
    """
    Build a parser using the params set using the option and positional decorators

    Used by the command and command_method decorators to build a parser using
    the arguments that have been added by the option and positional decorators

    param: func - The function being decorated
    param: args - A string containing command line like arguments
    """
    params = _get_params(func)
    del func.__yoga_params__
    params.options.reverse()
    params.positionals.reverse()
    parser = ArgumentParser()
    for o in params.options:
        parser.add_option(*o)

    for p in params.positionals:
        parser.add_positional(p)
    return parser


def command_method(func):
    """
    Automatically parse arguments for a method

    This decorator is setup so that the final function call is
    object.method(arg_string). Useful for all the same things as the normal
    command decorator except works with classes
    """
    return ParseMethod(func, _make_parser(func))

def command(func):
    """
    Automatically parse argument string into function args

    This decorator changes the function to accept a string containing command
    line like arguments and parse them into the function's real arguments
    """
    return ParseFunc(func, _make_parser(func))

def option(match, nargs=0):
    """
    Add an option to the command

    Works with the command or command_method decorators to parse arguments.
    Used to specify a single option to be parsed from the arguments string

    param: match - A string containing the flag for this option. See ArgumentParser.add_option for more
    param: nargs - Number of positional arguments that follow this one. Can be
            >=0 or =='*' See ArgumentParser.add_option for more
    """
    def decorator(func):
        _get_params(func).options.append((match, nargs))
        return func
    return decorator

def positional(match):
    """
    Add a positional argument to the command

    Works with the command or command_method decorators to parse arguments.
    Used to specify a single positional argument to be parsed from the arguments string

    param: match - A string matching an argument to the decorated function.
    """
    def decorator(func):
        _get_params(func).positionals.append(match)
        return func
    return decorator
