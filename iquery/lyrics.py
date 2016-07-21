# -*- coding: utf-8 -*-

"""
iquery.lyrics
~~~~~~~~~~~~~

Lyric query from `http://www.xiami.com`.
"""

import re
from bs4 import BeautifulSoup
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
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def __repr__(self):
        return '<SongPage url={!r}>'.format(self.url)

    @property
    def song_info(self):
        """This may contains: album, singer, lyric author, tune author."""
        text = self.soup.find(id='albums_info').text
        return text.replace(' ', '') \
                   .replace('\n\n', '') \
                   .replace('：\n', '：')

    @property
    def song_lyric(self):
        try:
            lyric = self.soup.find(class_='lrc_main').text.strip()
        except AttributeError:
            lyric = '暂无歌词'
        return lyric

    def pretty_print(self):
        print(colored.green(self.song_info))
        print(self.song_lyric)


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
