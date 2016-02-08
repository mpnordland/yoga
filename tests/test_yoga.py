import unittest
from yoga import ArgumentParser, ArgumentError

class TestPositionalArguments(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def test_single_positional(self):
        self.parser.add_positional("foo")
        result = self.parser.parse("baz")
        self.assertEqual(result, {"foo": "baz"})

        with self.assertRaises(ArgumentError):
            self.parser.parse("")
    def test_multiple_positionals(self):
        self.parser.add_positional("foo")
        self.parser.add_positional("bar")
        self.parser.add_positional("baz")
        result = self.parser.parse("ham spam eggs")
        self.assertEqual(result, {'foo':'ham', 'bar': 'spam', 'baz': 'eggs'})

        with self.assertRaises(ArgumentError):
            self.parser.parse("")
        with self.assertRaises(ArgumentError):
            self.parser.parse("ham spam")
        with self.assertRaises(ArgumentError):
            self.parser.parse("spam")
        with self.assertRaises(ArgumentError):
            self.parser.parse("ham eggs spam bacon")

class TestOptionArguments(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def test_single_option(self):
        self.parser.add_option("-foo")
        result = self.parser.parse("-foo")
        self.assertEqual(result, {"foo":True})

        result = self.parser.parse("")
        self.assertEqual(result, {'foo': False})




    def test_multiple_options(self):
        all_present={'foo': True, 'bar': True, 'baz': True}
        foo_absent={'foo': False, 'bar': True, 'baz': True}
        bar_absent={'foo': True, 'bar': False, 'baz': True}
        baz_absent={'foo': True, 'bar': True, 'baz': False}
        all_absent={'foo': False, 'bar': False, 'baz': False}
        self.parser.add_option('-foo')
        self.parser.add_option('-bar')
        self.parser.add_option('-baz')

        result = self.parser.parse('-foo -bar -baz')
        self.assertEqual(result, all_present)

        result = self.parser.parse('-baz -foo -bar')
        self.assertEqual(result, all_present)

        self.assertEqual(self.parser.parse('-bar -baz'), foo_absent)
        self.assertEqual(self.parser.parse('-foo -baz'), bar_absent)
        self.assertEqual(self.parser.parse('-foo -bar'), baz_absent)

        self.assertEqual(self.parser.parse(''), all_absent)

    def test_misc(self):
        self.parser.add_option("--foo")
        self.parser.add_option("--bar", nargs=1)
        self.assertEqual(self.parser.parse('--foo'), {'foo':True})
        self.assertEqual(self.parser.parse(''), {'foo':False})
        self.assertEqual(self.parser.parse(['--foo']), {'foo':True})
        self.assertEqual(self.parser.parse([]), {'foo':False})
        self.assertEqual(self.parser.parse('--bar one'),
                         {'bar': 'one', 'foo': False})

        with self.assertRaises(TypeError):
            self.parser.parse({'foo': True})



class TestOptionsWithArguments(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def test_single_option_with_argument(self):
        self.parser.add_option('-foo', nargs=2)
        self.assertEqual(self.parser.parse('-foo ham spam'),
                         {'foo': ['ham', 'spam']})

        # You don't have to pass the option, no option is required
        self.assertEqual(self.parser.parse(''), {})

        # You have to provide all the arguments
        with self.assertRaises(ArgumentError):
            self.parser.parse('-foo ham')

        # You can't have less than zero args
        with self.assertRaises(ValueError):
            self.parser.add_option('-bar', nargs=-1)

        # nargs must be an int greater than 0 or '*'. Nothing else
        with self.assertRaises(ValueError):
            self.parser.add_option('-baz', nargs='b')

        # Having numerical options makes passing negative numbers hard.
        # There aren't really many places where you need them either.
        with self.assertRaises(ValueError):
            self.parser.add_option('-1')

        with self.assertRaises(ArgumentError):
            self.parser.parse("-quxx")



    def test_single_option_with_varargs(self):
        # This option should take zero or more until the next option (not
        # positional)
        self.parser.add_option('-foo', nargs='*')

        self.assertEqual(self.parser.parse('-foo one two three'),
                         {'foo': ['one', 'two', 'three']})

        self.assertEqual(self.parser.parse('-foo -1 -2 -3'),
                         {'foo': ['-1', '-2', '-3']})

        self.assertEqual(self.parser.parse('-foo one two'),
                         {'foo':['one', 'two']})

        self.assertEqual(self.parser.parse('-foo'), {'foo': []})

        self.assertEqual(self.parser.parse(''), {})

    def test_multiple_options_with_varargs(self):
        self.parser.add_option('-foo', nargs='*')
        self.parser.add_option('-baz', nargs='*')
        self.parser.add_option('-bar')
        self.assertEqual(self.parser.parse('-foo one two'),
                         {'foo':['one','two'],'bar': False})
        self.assertEqual(self.parser.parse('-foo one two -bar'),
                         {'foo':['one', 'two'], 'bar':True})
        self.assertEqual(self.parser.parse('-foo one two -bar -baz spam ham eggs'),
                         {'foo':['one','two'], 'bar':True, 'baz': ["spam", "ham", "eggs"]})

class TestPositionalAndOptions(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def test_postionals_and_options(self):
        self.parser.add_positional("enemy")
        self.parser.add_option("-em", nargs='*')
        self.parser.add_option("-am", nargs='*')

        self.assertEqual(self.parser.parse("ham -am 1 1 1 2 -1 -em 3 2 1 -1"),
                         {'enemy': 'ham', 'am': ['1', '1', '1', '2', '-1'], 'em':
                          ['3', '2', '1', '-1']})
