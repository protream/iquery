# -*- coding: utf-8 -*-

"""
iquery.movies
~~~~~~~~~~~~~~

Movies query and display. The datas come
from:
    m.douban.com/movie
"""

import re
import textwrap
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from .utils import colored, requests_get, exit_after_echo


__all__ = ['query']

QUERY_URL = ('https://frodo.douban.com/jsonp/'
             'subject_collection/movie_showing/items')


class MoviesCollection(object):

    """Docstring for HotAndComingMovies. """

    header = '编号 电影名称+上映日期 导演+主演+类型 豆瓣评分'.split()

    def __init__(self, rows):
        self._rows = rows

    def __len__(self):
        return len(self._rows)

    @property
    def movies(self):
        for idx, row in enumerate(self._rows):
            rating = row.get('rating')
            # douban score
            score = '{:.1f}'.format(rating.get('value')) if rating else '暂无'
            infos = row['info'].split('/')
            if re.match('\d', infos[-1]):
                time = infos[-1:]
                infos = '/'.join(infos[:-1])
            else:
                time = infos[-2:]
                infos = '/'.join(infos[:-2])
            m = [
                idx + 1,
                '\n'.join([
                    colored.green(row['title']),
                    colored.red(time[0][:10]),
                ]),
                infos,
                score
            ]
            yield m

    def _get_movie_summary(self, num):
        url = self._rows[num - 1].get('url')
        r = requests_get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        s = re.sub(r'\s+', '', soup.find(property="v:summary").text)
        print(textwrap.fill(colored.green(s), 40, initial_indent=''))

    def pretty_print(self):

        pt = PrettyTable()
        pt._set_field_names(self.header)
        for m in self.movies:
            pt.add_row(m)
        print(pt)

        print('输入编号获取剧情简介:')
        while True:
            raw = input('>> ')
            if raw in ('q', 'quit'):
                exit()
            try:
                num = int(raw)
            except ValueError:
                print('Invalid number.')
                continue

            if (num - 1) in range(len(self)):
                self._get_movie_summary(num)
            else:
                print('Invalid number.')


def query():
    """Query hot movies infomation from douban."""

    r = requests_get(QUERY_URL)

    try:
        rows = r.json()['subject_collection_items']
    except (IndexError, TypeError):
        rows = []

    return MoviesCollection(rows)
