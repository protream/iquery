# -*- coding: utf-8 -*-

"""
iquery.utils
~~~~~~~~~~~~~

A simple args parser and a color wrapper.
"""

import sys
import random
import requests
from requests.exceptions import ConnectionError, Timeout


__all__ = ['args', 'colored', 'requests_get', 'exit_after_echo']


def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    exit(1)


def requests_get(url, **kwargs):
    USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
         'Chrome/19.0.1084.46 Safari/536.5'),
        ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
         'Safari/536.5')
    )
    try:
        r = requests.get(
            url,
            timeout=12,
            headers={'User-Agent': random.choice(USER_AGENTS)}, **kwargs
        )
    except ConnectionError:
        exit_after_echo('Network connection failed.')
    except Timeout:
        exit_after_echo('timeout.')
    return r


class Args(object):

    """A simple customed args parser for `iquery`."""

    def __init__(self, args=None):
        self._args = sys.argv[1:]
        self._argc = len(self)

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
        return self._argc == 0

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
        if self._argc not in (2, 3):
            return False
        if is_show_type(arg):
            return True
        return False

    @property
    def is_querying_train(self):
        if self._argc not in (3, 4):
            return False
        if self.is_querying_show:
            return False
        if self._argc == 4:
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
    def is_querying_lyric(self):
        arg = self.get(0)
        if arg == '-l':
            return True
        return False

    @property
    def is_querying_putian_hospital(self):
        return self.get(0) == '-p' and self._argc in (2, 3)

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

    @property
    def as_lyric_query_params(self):
        return '+'.join(self._args[1:])


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
