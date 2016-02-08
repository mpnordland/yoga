import unittest
from yoga import command, command_method, option, positional

class TestDecorators(unittest.TestCase):
    def test_single_positional_decorator(self):
        @command
        @positional("foo")
        def test_command(foo):
            return foo

        self.assertEqual(test_command("blah"), "blah")

    def test_multiple_positionals_decorator(self):
        @command
        @positional("foo")
        @positional("bar")
        @positional("baz")
        def test_command(foo, bar, baz):
            print(foo, bar, baz)
            return foo, bar, baz

        self.assertEqual(test_command("ham spam eggs"), ("ham", "spam", "eggs"))

    def test_single_option_decorator(self):
        @command
        @option("-foo")
        def one_flag(foo):
            return foo

        self.assertEqual(one_flag("-foo"), True)
        self.assertEqual(one_flag(""), False)

        @command
        @option("-bar", nargs=2)
        def one_option_with_varargs(bar):
            return bar

        self.assertEqual(one_option_with_varargs("-bar one two"), ['one', 'two'])


    def test_method_option_decorator(self):
        class Test(object):

            @command_method
            @option("-foo")
            def one_flag(self, foo):
                return foo

            @command_method
            @option("-foo", nargs=2)
            def one_option_with_positionals(self, foo=None):
                return foo

            @command_method
            @option("-foo", nargs='*')
            def one_option_with_varargs(self, foo):
                return foo

        test = Test()
        self.assertEqual(test.one_flag("-foo"), True)
        self.assertEqual(test.one_flag(""), False)
        self.assertEqual(test.one_option_with_positionals("-foo one two"), ['one', 'two'])
        self.assertEqual(test.one_option_with_positionals(""), None)
        self.assertEqual(test.one_option_with_varargs("-foo one two three"), ['one', 'two', 'three'])

    def test_method_positional_decorator(self):
        class Test(object):
            def __init__(self):
                self.foo = "bar"

            @command_method
            @positional("greeting")
            def one_positional(self, greeting):
                return "{} {}".format(greeting, self.foo)

            @command_method
            @positional('foo')
            @positional('bar')
            @positional('baz')
            def multiple_positionals(self, foo, bar, baz):
                return foo, bar, baz

        test = Test()
        self.assertEqual(test.one_positional("Hello"), "Hello bar")
        self.assertEqual(test.multiple_positionals("ham spam eggs"), ('ham', 'spam', 'eggs'))

    def test_mixed_decorators(self):
        class Test(object):
            @command_method
            @positional("foo")
            @option("-bar")
            @option("-baz", nargs=2)
            def mixed_arguments(self, foo, bar, baz):
                return foo, bar, baz

        test = Test()

        self.assertEqual(test.mixed_arguments("ham -bar -baz spam eggs"), ("ham", True, ['spam', 'eggs']))

