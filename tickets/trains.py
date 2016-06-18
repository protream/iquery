# -*- coding: utf-8 -*-

"""
    tickets.trains
    ~~~~~~~~~~~~~~

    Train tickets model.
"""

import os
import re
import sys
import json
from datetime import datetime
from collections import OrderedDict
from .utils import colored, exit_after_echo

import requests
from prettytable import PrettyTable
from requests.exceptions import ConnectionError


__all__ = ['TrainTicketsQuery']


QUERY_URL = 'https://kyfw.12306.cn/otn/lcxxcx/query'

# ERROR MSG
FROM_STATION_NOT_FOUND = 'From station not found.'
TO_STATION_NOT_FOUND = 'To station not found.'
INVALID_DATE = 'Invalid query date.'
NETWORK_CONNECTION_FAIL = 'Network connection failed.'
TRAIN_NOT_FOUND = 'No result.'


class TrainsCollection(object):

    """A set of raw datas from a query."""

    headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()

    def __init__(self, rows, opts):
        self._rows = rows
        self._opts = opts

    def __repr__(self):
        return '<TrainsCollection size={}>'.format(len(self))

    def __iter__(self):
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                yield next(self)
            i += 1

    def __len__(self):
        return len(self._rows)

    def _get_duration(self, row):
        duration = row.get('lishi').replace(':', '小时') + '分钟'
        # take 0 hour , only show minites
        if duration.startswith('00'):
            return duration[4:]
        # take <10 hours, show 1 bit
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        """Filter rows according to `headers`"""
        for row in self._rows:
            train_no = row.get('station_train_code')
            initial = train_no[0].lower()
            if not self._opts or initial in self._opts:
                train = [
                    # Column: '车次'
                    train_no,
                    # Column: '车站'
                    ''.join([
                        colored.green(row.get('from_station_name')),
                        '\n',
                        colored.red(row.get('to_station_name')),
                    ]),
                    # Column: '时间'
                    ''.join([
                        colored.green(row.get('start_time')),
                        '\n',
                        colored.red(row.get('arrive_time')),
                    ]),
                    # Column: '历时'
                    self._get_duration(row),
                    # Column: '商务'
                    row.get('swz_num'),
                    # Column: '一等'
                    row.get('zy_num'),
                    # Column: '二等'
                    row.get('ze_num'),
                    # Column: '软卧'
                    row.get('rw_num'),
                    # Column: '硬卧'
                    row.get('yw_num'),
                    # Column: '软座'
                    row.get('rz_num'),
                    # Column: '硬座'
                    row.get('yz_num'),
                    # Column: '无座'
                    row.get('wz_num')
                ]
                yield train

    def pretty_print(self):
        """Use `PrettyTable` to perform formatted outprint."""
        pt = PrettyTable()
        if len(self) == 0:
            pt._set_field_names(['Sorry,'])
            pt.add_row([TRAIN_NOT_FOUND])
        else:
            pt._set_field_names(self.headers)
            for train in self.trains:
                pt.add_row(train)
        print(pt)


class TrainTicketsQuery(object):

    """Docstring for TrainTicketsCollection. """

    def __init__(self, from_station, to_station, date, opts=None):

        self.from_station = from_station
        self.to_station = to_station
        self.date = date
        self.opts = opts

    def __repr__(self):
        return 'TrainTicketsQuery from={} to={} date={}'.format(
            self._from_station, self._to_station, self._date
        )

    @property
    def stations(self):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'datas', 'stations.dat'
        )
        d = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                name, telecode = line.split()
                d.setdefault(name, telecode)
        return d

    @property
    def _from_station_telecode(self):
        code = self.stations.get(self.from_station)
        if not code:
            exit_after_echo(FROM_STATION_NOT_FOUND)
        return code

    @property
    def _to_station_telecode(self):
        code = self.stations.get(self.to_station)
        if not code:
            exit_after_echo(TO_STATION_NOT_FOUND)
        return code

    @property
    def _valid_date(self):
        date = self.date.strip()
        try:
            date_token = self._date_format(date)
            if date_token is None:
                raise ValueError(self.date)
            date = datetime.strptime(date, date_token.join(('%Y', '%m', '%d')))
        except ValueError:
            exit_after_echo(INVALID_DATE)
        diff = date - datetime.today()
        if diff.days not in range(-1, 50):
            exit_after_echo(INVALID_DATE)
        return datetime.strftime(date, '%Y-%m-%d')

    @staticmethod
    def _date_format(date):
        result = re.findall('\D{1}', date)
        result_len = len(result)
        if result_len == 0:
            return ''
        elif result_len == 2:
            if result[0] == result[1]:
                result = result[0]
                if result == '%':
                    return '%%'
                else:
                    return result
        return None

    def _build_params(self):
        """Have no idea why wrong params order can't get data.
        So, use `OrderedDict` here.
        """
        d = OrderedDict()
        d['purpose_codes'] = 'ADULT'
        d['queryDate'] = self._valid_date
        d['from_station'] = self._from_station_telecode
        d['to_station'] = self._to_station_telecode
        return d

    def query(self):

        params = self._build_params()

        try:
            r = requests.get(QUERY_URL, params=params, verify=False)
        except ConnectionError:
            exit_after_echo(NETWORK_CONNECTION_FAIL)

        try:
            rows = r.json()['data']['datas']
        except KeyError:
            rows = []

        return TrainsCollection(rows, self.opts)
