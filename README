yoga is a flexible argument parser for command line like arguments.

yoga is can be thought of as an acronym of YOu Got Arguments, but this is not
necessary.

A good explanation of what yoga does begins with what it does not:
    * magic - yoga strives to be as magic free as possible yoga never gets any
      data from anywhere other than what you give it.

    * run your app - yoga is a parser, and should never quit your program. It
      may raise exceptions which are your job to handle.

    * interpret arguments - That's your job.

    * allow numeric options - These make negative number positionals hard to
      distinguish

    * generate help documentation - yoga is a parser, as a part of the no magic
      rule it adds no options you don't specify. Features to enable you to
      query the list of arguments may be added later to help you to do it
      yourself

yoga seeks to be as flexible as possible within these constraints.

yoga has two kinds of arguments: positionals and options. Positionals are
required (with one exception) and options are not. Positionals must be passed in
the same order that they are added. Options may be passed in any order and
interspersed freely between positionals. Options may take additional positional
arguments after the initial option flag. There are two ways to do this: a
specific, required number of positionals, or a variable, zero or larger number
of positionals until the next option argument.

There are two API styles: parser based and decorator based.

#Parser Based
The parser based api works like argparse, but isn't a drop in replacement by
far. Create an instance of `ArgumentParser` and then call `add_positional` and
`add_option` to add arguments. To parse arguments, pass a string of arguments to
`parse`

    parser = ArgumentParser()
    parser.add_positional("name")
    parser.add_option("--greeting", nargs=1)
    result = parser.parse("World --greeting Hello")
    #result = {'name': 'World', 'greeting': 'Hello'}

#Decorator based
Similar to the parser based api, but a bit easier to use. Just define a function
and decorate it with the `command` and the `option` and `positional` decorators.

    @command
    @positional("name")
    @option("--greeting", nargs=1)

    #define defaults for options like normal
    def hello(name, greeting="Hello"):
        return "{} {}".format(greeting, name)

    hello("World")
    # returns "Hello World"

    hello("World --greeting Bonjour")
    #returns "Bonjour World"

Methods can also be decorated using the `command_method` decorator. Just define
your method like normal and use the `command_method` instead of `command` and
the `option` and `positional` decorators like normal.

    class Greeter:
        def __init__(self):
            #This greeter can remember greetings
            self.greetings = set()
        @command_method
        @positional("name")
        @option("--greeting", nargs=1)
        def hello(self, name, greeting="Hello")
            self.greetings.add(greeting)
            return "{} {}".format(greeting, name)

    greeter = Greeter()

    greeter.hello("World")
    #returns "Hello World"

    greeter.hello("World --greeting Bonjour")
    #returns "Bonjour World"

Both APIs raise ArgumentError when parsing the passed arguments fails.

You may use a list of arguments instead of a space separated string.
