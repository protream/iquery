# -*- coding: utf-8 -*-

"""Train tickets query via the command line.

Usage:
    tickets [options] <from> <to> <date>

Arguments:
    from             出发站
    to               到达站
    date             查询日期

Options:
    -h, --help       显示该帮助菜单.
    -d               动车
    -g               高铁
    -k               快速
    -t               特快
    -z               直达

Examples:
    tickets 南京 北京 201671
    tickets -k  南京南 上海 2016-7-1
    tickets -dg 上海虹桥 北京西 2016/7/1
"""

import os
import re
import sys
import json
from datetime import datetime
from collections import OrderedDict
from _compat import to_unicode

import requests
from docopt import docopt
from prettytable import PrettyTable
from requests.exceptions import ConnectionError

try:
    from requests.packages.urllib3.exceptions import (
        SNIMissingWarning,
        InsecureRequestWarning,
        InsecurePlatformWarning
    )
    # Not show warings
    requests.packages.urllib3.disable_warnings(SNIMissingWarning)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
except ImportError:
    pass


def _load_stations():
    filepath = os.path.join(os.path.dirname(__file__), 'stations.dat')
    stations = {}
    with open(filepath, 'rb') as f:
        for line in f.readlines():
            name, telecode = line.split()
            stations[to_unicode(name)] = to_unicode(telecode)
    return stations


stations = _load_stations()

QUERY_URL = 'http://kyfw.12306.cn/otn/lcxxcx/query'


def colorit(color, msg):
    """Wrap `msg` with color. If `msg` is not string, do nothing."""
    scheme = {
        'red': '\033[91m',
        'green': '\033[92m',

        # No color
        'nc': '\033[0m'
    }
    # color value
    cv = scheme.get(color)
    if not cv:
        raise KeyError('color is not defined.')
    nc = scheme.get('nc')
    return ''.join([cv, msg, nc])


class TrainsCollection(object):
    """A set of raw datas from a query.

    :opts: '' or a subset of 'dgktz'
    """

    headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()

    def __init__(self, rows, opts):
        self._rows = rows
        self._opts = opts

    def __iter__(self):
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                yield next(self)
            i += 1

    def _get_duration(self, row):
        duration = row.get('lishi').replace(':', u'小时') + u'分钟'
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
                        colorit('green', row.get('from_station_name')),
                        '\n',
                        colorit('red', row.get('to_station_name'))
                    ]),
                    # Column: '时间'
                    ''.join([
                        colorit('green', row.get('start_time')),
                        '\n',
                        colorit('red', row.get('arrive_time'))
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

    def export(self):
        """Use `PrettyTable` to perform formatted outprint."""
        pt = PrettyTable()
        pt._set_field_names(self.headers)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def get_valid_date(raw_date):
    """Check if the date is valid, if is, return a formatted
    datetime, otherwise, return ''.

    :raw_date: A user input string date.
    """
    raw_date = re.sub(r'[-/\:,]+', '', raw_date)
    try:
        date = datetime.strptime(raw_date, '%Y%m%d')
    except ValueError:
        return ''
    diff = date - datetime.today()
    if diff.days not in range(-1, 50):
        return ''
    return datetime.strftime(date, '%Y-%m-%d')


def build_params(from_station, to_station, date):
    """Have no idea why wrong params order can't get data.
    So, use `OrderedDict` here.

    :param from_station: the `from` station telecode
    :param to_station: `to` station telecode
    :param date: query date
    """
    d = OrderedDict()
    d['purpose_codes'] = 'ADULT'
    d['queryDate'] = date
    d['from_station'] = from_station
    d['to_station'] = to_station
    return d


def cli():
    # Parse the command-line arguments.
    arguments = docopt(__doc__)

    from_station_code = stations.get(to_unicode(arguments['<from>']))
    if not from_station_code:
        print('Seems that no this station where you from.')
        exit()

    to_station_code = stations.get(to_unicode(arguments['<to>']))
    if not to_station_code:
        print('Seems that no this station where you going to.')
        exit()

    valid_date = get_valid_date(to_unicode(arguments['<date>']))
    if not valid_date:
        print('Not a valid date.')
        exit()

    # Transform valid options to a string.
    opts = ''.join(o[1] for o in arguments if o in '-d-g-k-t-z' and arguments[o])

    params = build_params(from_station_code, to_station_code, valid_date)
    try:
        resp = requests.get(QUERY_URL, params=params, verify=False)
    except ConnectionError:
        print(colorit('red', 'Network connection fail.'))
        exit()

    try:
        rows = resp.json()['data']['datas']
    except KeyError:
        print(colorit('green', 'No train available.'))

    trains = TrainsCollection(rows, opts)

    trains.export()


if __name__ == '__main__':
    cli()
