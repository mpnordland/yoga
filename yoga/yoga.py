import collections

class ArgumentError(Exception):
    pass

class Option(object):
    """
    This class holds an option and the number of arguments it takes
    name: name of the argument e.g. --option
    nargs: number of arguments or '*' to capture all positional arguments until the next
            option
    """
    def __init__(self, name, nargs):
        self.match= name
        self.name = name.strip('-')
        self.nargs = nargs



class ArgumentParser(object):
    def __init__(self):
        self._positionals = []
        self._options = []

    def add_positional(self, name):
        self._positionals.append(name)

    def add_option(self, match, nargs=0):
        """
        Options should start with at least one '-' but can have any number
        greater than that. -foo and --foo would both produce a 'foo' entry in
        the output from parse. DON'T add two separate options like that. That
        may result in arguments getting lost or the wrong options applied.
        """
        if match.strip('-')[0].isnumeric():
            raise ValueError("Cannot begin an option with a number")

        if isinstance(nargs, str) and nargs != '*':
                raise ValueError("Invalid nargs value {}".format(nargs))
        elif isinstance(nargs, int) and nargs < 0:
            raise ValueError("Cannot have negative number of arguments")
        self._options.append(Option(match, nargs))

    def get_optional(self, match):
        for opt in self._options:
            if opt.match == match:
                return opt
        raise ArgumentError("Option doesn't exist {}".format(match))

    def get_variable_options(self, args):
        options = []
        for a in args:
            if a.startswith('-'):
                striped_a = a.strip('-')
                if not striped_a.isnumeric():
                    break
            options.append(a)
        del args[:len(options)]
        return options

    def process_optional(self, args):
        arg = args.pop(0)
        opt = self.get_optional(arg)
        result = (opt.name, True)
        if opt.nargs != 0:
            if opt.nargs == '*':
                result = (opt.name, self.get_variable_options(args))
            elif opt.nargs == 1:
                result=(opt.name, args.pop(0))
            else:
                if opt.nargs > len(args):
                    raise ArgumentError("Not enough required arguments to option")
                result=(opt.name, args[:opt.nargs])
                del args[:opt.nargs]
        return result


    def parse(self, args):
        if isinstance(args, str):
            args = args.split()
        elif not isinstance(args, collections.Sequence):
            raise TypeError("args is not a sequence")
        parsed = {}
        positional_pos = 0
        while args:
            arg = args[0]
            if arg.startswith('-'):
                name, val = self.process_optional(args)
                parsed[name] = val
            else:
                if positional_pos < len(self._positionals):
                    parsed[self._positionals[positional_pos]] = args.pop(0)
                    positional_pos += 1
                else:
                    raise ArgumentError("Invalid positional argument {}".format(arg))


        if len(self._positionals) > 0 and positional_pos != len(self._positionals):
            raise ArgumentError("Missing required positional arguments")

        # Options without following args need to show up as False if they were
        # not present
        for opt in self._options:
            if opt.name not in parsed.keys() and opt.nargs == 0:
                    parsed[opt.name] = False

        return parsed


