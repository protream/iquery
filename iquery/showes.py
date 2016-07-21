# -*- coding: utf-8 -*-

"""
iquery.showes
~~~~~~~~~~~~~~

Show tickets query and display. The datas come
from:
    www.damain.cn
"""

import os
import re
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import datetime, timedelta
from .utils import colored, requests_get, exit_after_echo


__all__ = ['is_show_type', 'query']

SHOWES_QUERY_URL = 'http://www.damai.cn/projectlist.do'

# ERR MSG
QUERY_DAYS_INVALID = 'Invalid days.'
CITY_NOT_FOUND = 'Sorry, your city is not supported.'
SHOW_NOT_FOUND = 'No result.'

# All supported show types and its query params.
SHOW_TYPES = {
    '演唱会': {'mcid': 1, 'ccid': ''},
    '音乐会': {'mcid': 2, 'ccid': ''},
    '音乐剧': {'mcid': 3, 'ccid': 22},
    '儿童剧': {'mcid': 3, 'ccid': 23},
    '歌舞剧': {'mcid': 3, 'ccid': 21},
    '话剧': {'mcid': 3, 'ccid': 19},
    '歌剧': {'mcid': 3, 'ccid': 20},
    '舞蹈': {'mcid': 4, 'ccid': ''},
    '相声': {'mcid': 5, 'ccid': 27},
    '魔术': {'mcid': 5, 'ccid': 28},
    '马戏': {'mcid': 5, 'ccid': 29},
    '杂技': {'mcid': 5, 'ccid': 30},
    '戏曲': {'mcid': 5, 'ccid': 31},
    '比赛': {'mcid': 6, 'ccid': ''}
}


is_show_type = frozenset(SHOW_TYPES.keys()).__contains__


class ShowesCollection(object):

    """A set of showes from a query."""

    #: The header of every column
    headers = '主题 票价 场馆 '.split()

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
        with open(filepath, 'r', encoding='utf-8') as f:
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
        st = SHOW_TYPES.get(self.show_type)
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
            theme = colored.green(item.find(class_='ico').a.text.strip())
            text = item.find(class_='mt10').text.strip()
            mix = re.sub('\s+', ' ', text).split('：')
            time = mix[1][:-3]
            place = mix[2][:-7]
            # display time below theme
            theme_time = '\n'.join([
                theme,
                colored.red(''.join([
                    '(', time, ')'
                ]))
            ])
            price = item.find(class_='price-sort').text.strip()
            rows.append([theme_time, price, place])
        return rows

    def query(self):
        params = self._build_params()
        rows = []

        while True:
            r = requests_get(SHOWES_QUERY_URL, params=params)
            soup = BeautifulSoup(r.text, 'html.parser')

            items = soup.find_all(class_='ri-infos')
            if not items:
                return ShowesCollection(rows)

            rows += self.parse(items)
            params['pageIndex'] += 1


def query(params):
    """`params` is a list, contains `city`, 'show_type`, `days`."""

    return ShowTicketsQuery(*params).query()
