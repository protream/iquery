# -*- coding: utf-8 -*-

"""
    tickets.utils
    ~~~~~~~~~~~~~

    A simple args parser and a color wrapper.
"""

import sys


__all__ = ['args', 'colored', 'exit_after_echo', 'is_show_type']


def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    exit()

show_types_list = (
    '演唱会 音乐会 比赛 话剧 歌剧 戏曲 相声 ' +
    '音乐剧 歌舞剧 儿童剧 舞蹈 杂技 马戏 魔术'
).split()


is_show_type = frozenset(show_types_list).__contains__


class Args(object):

    """A simple customed args parser for `tickets`."""

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
        arg = self.get(1)
        if len(self) not in (2, 3):
            return False
        if is_show_type(arg):
            return True
        return False

    @property
    def is_querying_train(self):
        if len(self) not in (3, 4):
            return False
        if self.is_querying_show:
            return False
        return True

    @property
    def is_querying_movie(self):
        arg = self.get(0)
        if arg in ('-m', '电影'):
            return True
        return False

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
