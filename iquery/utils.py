# -*- coding: utf-8 -*-

"""
iquery.utils
~~~~~~~~~~~~~

A simple args parser and a color wrapper.
"""

import sys


__all__ = ['args', 'colored', 'exit_after_echo']


def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    exit()


class Args(object):

    """A simple customed args parser for `iquery`."""

    def __init__(self, args=None):
        self._args = sys.argv[1:]

    def __repr__(self):
        return '<args {}>'.format(repr(self._args))

    def __len__(self):
        return len(self._args)

    @property
    def all(self):
        return self._args

    def get(self, idx):
        try:
            return self.all[idx]
        except IndexError:
            return None

    @property
    def is_null(self):
        return len(self.all) == 0

    @property
    def options(self):
        """Train tickets query options."""
        arg = self.get(0)
        if arg.startswith('-') and not self.is_asking_for_help:
            return arg[1:]
        return ''.join(x for x in arg if x in 'dgktz')

    def contain_show_type(self):
        arg = self.get(2)
        if is_show_type(arg):
            return arg
        return None

    @property
    def is_asking_for_help(self):
        arg = self.get(0)
        if arg in ('-h', '--help'):
            return True
        return False

    @property
    def is_querying_show(self):
        from .showes import is_show_type
        arg = self.get(1)
        if len(self) not in (2, 3):
            return False
        if is_show_type(arg):
            return True
        return False

    @property
    def is_querying_train(self):
        l = len(self)
        if l not in (3, 4):
            return False
        if self.is_querying_show:
            return False
        if l == 4:
            arg = self.get(0)
            if not arg.startswith('-'):
                return False
            if arg[1] not in 'dgktz':
                return False
        return True

    @property
    def is_querying_movie(self):
        arg = self.get(0)
        if arg in ('-m', '电影'):
            return True
        return False

    @property
    def is_querying_putian_hospital(self):
        return self.get(0) == '-p' and len(self) in (2, 3)

    @property
    def as_train_query_params(self):
        opts = self.options
        if opts:
            # apped valid options to end of list
            return self._args[1:] + [opts]
        return self._args

    @property
    def as_show_query_params(self):
        return self._args

    @property
    def as_hospital_query_params(self):
        return self._args[1:]


class Colored(object):

    """Keep it simple, only use `red` and `green` color."""

    RED = '\033[91m'
    GREEN = '\033[92m'

    #: no color
    RESET = '\033[0m'

    def color_str(self, color, s):
        return '{}{}{}'.format(
            getattr(self, color),
            s,
            self.RESET
        )

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)


args = Args()
colored = Colored()
