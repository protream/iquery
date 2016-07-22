# -*- coding: utf-8 -*-

"""
iquery.lyrics
~~~~~~~~~~~~~

Lyric query from `http://www.xiami.com`.
"""

import re
import pyquery
from pyquery import PyQuery
from prettytable import PrettyTable
from .utils import colored, requests_get, exit_after_echo


__all__ = ['query']

SONG_SEARCH_URL = 'http://www.xiami.com/search?key={}'
# ERR MSG
SONG_NOT_FOUND = 'Sorry, song not found.'


class SongPage(object):

    """The query song's page on xiami. """

    def __init__(self, song_url):
        self.url = song_url
        self.html_content = requests_get(self.url).text

        #: pyquery object
        self._d = PyQuery(self.html_content)

    def __repr__(self):
        return '<SongPage url={!r}>'.format(self.url)

    @property
    def song_infos(self):
        # TODO:
        pass

    @property
    def lyric(self):
        raw = self._d('.lrc_main').html()
        if raw:
            lyric = raw.strip().replace('<br/>', '') \
                               .replace('&#13;', '\n') \
                               .replace('\n\n', '\n')
        else:
            exit_after_echo(SONG_NOT_FOUND)
        return lyric

    def pretty_print(self):
        print('\n' + self.lyric)


def query(song_name):
    """CLI:

    $ iquery -l song_name
    """
    r = requests_get(SONG_SEARCH_URL.format(song_name))

    try:
        # Get the first result.
        song_url = re.search(r'(http://www.xiami.com/song/\d+)', r.text).group(0)
    except AttributeError:
        exit_after_echo(SONG_NOT_FOUND)

    return SongPage(song_url)
