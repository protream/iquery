# -*- coding: utf-8 -*-

"""
    tickets.utils
    ~~~~~~~~~~~~~

    Some tool.
"""

import sys
import colorama


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
        if len(self.all) not in (2, 3):
            return False
        if is_show_type(arg):
            return True
        return False

    @property
    def is_querying_train(self):
        if len(self.all) not in (3, 4):
            return False
        if self.is_querying_show:
            return False
        return True

    @property
    def as_train_query_params(self):
        opts = self.options
        if opts:
            # apped valid options to end of list
            return self.all[1:] + [opts]
        return self.all

    @property
    def as_show_query_params(self):
        return self.all


class Colored(object):

    """A simple wrapper based on colorama.

    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL

    """

    def color_str(self, color, s, style='NORMAL'):
        return '{}{}{}{}'.format(
            getattr(colorama.Fore, color),
            getattr(colorama.Style, style),
            s,
            colorama.Style.RESET_ALL
        )

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)


args = Args()
colored = Colored()
