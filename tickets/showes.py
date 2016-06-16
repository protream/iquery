# -*- coding: utf-8 -*-

"""
    tickets.showes
    ~~~~~~~~~~~~~~

    Show tickets model.
"""

import os
import re
import sys
from .utils import colored

import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import datetime, timedelta
from requests.exceptions import ConnectionError


__all__ = ['ShowTicketsQuery']


SHOWES_QUERY_URL = 'http://www.damai.cn/projectlist.do'

# ERROR MSG
QUERY_DAYS_INVALID = 'Invalid days.'
CITY_NOT_FOUND = 'City not found.'
SHOW_NOT_FOUND = 'No result.'
NETWORK_CONNECTION_FAIL = 'Network connection failed.'


class ShowesCollection(object):

    """A set of showes from a query."""

    #: The header of every column
    headers = '主题 时间 场馆 票价'.split()

    def __init__(self, rows):
        self._rows = rows

    def __repr__(self):
        return '<ShowTicketsCollection size={}>'.format(len(self))

    def __len__(self):
        return len(self._rows)

    def pretty_print(self):
        pt = PrettyTable()
        if len(self) == 0:
            pt._set_field_names(['Sorry,'])
            pt.add_row([SHOW_NOT_FOUND])
        else:
            pt._set_field_names(self.headers)
        for row in self._rows:
            pt.add_row(row)
        print(pt)


class ShowTicketsQuery(object):

    """Perform a show query."""

    #: show query params
    show_types = {
        '演唱会': {'mcid': 1, 'ccid': ''},
        '音乐会': {'mcid': 2, 'ccid': ''},
        '话剧': {'mcid': 3, 'ccid': 19},
        '歌剧': {'mcid': 3, 'ccid': 20},
        '音乐剧': {'mcid': 3, 'ccid': 22},
        '儿童剧': {'mcid': 3, 'ccid': 23},
        '歌舞剧': {'mcid': 3, 'ccid': 21},
        '舞蹈': {'mcid': 4, 'ccid': ''},
        '相声': {'mcid': 5, 'ccid': 27},
        '魔术': {'mcid': 5, 'ccid': 28},
        '马戏': {'mcid': 5, 'ccid': 29},
        '杂技': {'mcid': 5, 'ccid': 30},
        '戏曲': {'mcid': 5, 'ccid': 31},
        '比赛': {'mcid': 6, 'ccid': ''}
    }

    def __init__(self, city, show_type, days=15):
        self.city = city
        self.show_type = show_type
        self.days = days

    def __repr__(self):
        return '<ShowTicketsQuery city={} types={} days={}>'.format(
            self._city, self._type, self._days
        )

    @property
    def cities(self):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'datas', 'cities.dat'
        )
        d = {}
        with open(filepath, 'r') as f:
            for line in f.readlines():
                name, number = line.split()
                d.setdefault(name, int(number))
        return d

    @property
    def _city_id(self):
        ci = self.cities.get(self.city)
        if not ci:
            exit_after_echo(CITY_NOT_FOUND)
        return ci

    @property
    def _show_type(self):
        st = self.show_types.get(self.show_type)
        if not st:
            exit_after_echo(SHOW_NOT_FOUND)
        return st

    @property
    def date_range(self):
        """Generate date range according to the `days` user input."""
        try:
            days = int(self.days)
        except ValueError:
            exit_after_echo(QUERY_DAYS_INVALID)

        if days < 1:
            exit_after_echo(QUERY_DAYS_INVALID)
        start = datetime.today()
        end = start + timedelta(days=days)
        return (
            datetime.strftime(start, '%Y-%m-%d'),
            datetime.strftime(end, '%Y-%m-%d')
        )

    def _build_params(self):
        start, end = self.date_range
        return dict(
            cityID=self._city_id, isText=1,
            pageIndex=1, startDate=start,
            endDate=end, order=2,
            **self._show_type
        )

    def parse(self, items):
        """Parse `主题`, `时间`, `场馆`, 票价` in every item."""
        rows = []
        for i, item in enumerate(items):
            color = colored.green if i & 1 else colored.red
            theme = color(item.find(class_='ico').a.text.strip())
            text = item.find(class_='mt10').text.strip()
            mix = re.sub('\s+', ' ', text).split('：')
            time = mix[1][:-3]
            place = color(mix[2][:-7])
            price = item.find(class_='price-sort').text.strip()
            rows.append([theme, time, place, price])
        return rows

    def query(self):
        params = self._build_params()
        rows = []
        while True:
            try:
                r = requests.get(SHOWES_QUERY_URL, params=params)
            except ConnectionError:
                exit_after_echo(NETWORK_CONNECTION_FAIL)
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all(class_='ri-infos')
            if not items:
                return ShowesCollection(rows)
            rows += self.parse(items)
            params['pageIndex'] += 1
