# coding: utf-8

"""Train tickets query via the command line.

Usage:
    tickets [options] <from> <goto> <date>

Arguments:
    from             出发站
    goto             到达站
    date             查询日期

Options:
    -h, --help       显示该帮助菜单.
    -d               动车
    -g               高铁
    -k               快速
    -t               特快
    -z               直达

Examples:
    tickets 南京 北京 20160707
    tickets -k  南京南 上海 2016-07-07
    tickets -dg 上海虹桥 北京西 2016/07/07

"""

import re
import sys
import json
import requests

from datetime import datetime
from docopt import docopt
from stations import stations
from prettytable import PrettyTable
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import (
    SNIMissingWarning,
    InsecureRequestWarning,
    InsecurePlatformWarning
)


# For Python2
if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# Not show warings
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


QUERY_URL = 'http://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'


def colorit(color, msg):
    """Wrap `msg` with color, default red. If `msg` is not string
    , do nothing."""
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
    if not isinstance(msg, str):
        return
    nc = scheme.get('nc')
    return ''.join([cv, msg, nc])


class TrainsCollection(object):
    """A set of trains from a query."""

    headers = [
        '车次',
        '车站',
        '时间',
        '历时',
        '商务',
        '一等',
        '二等',
        '软卧',
        '硬卧',
        '软座',
        '硬座',
        '无座'
    ]

    def __init__(self, rows, options):
        self._rows = rows
        self._options = options

    def __iter__(self):
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                yield next(self)
            i += 1

    def _get_time_duration(self, row):
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
        """Filter rows accord to the headers"""
        for row in self._rows:
            train = [
                # Column: '车次'
                row.get('station_train_code'),
                # Column: '车站'
                ''.join([colorit('green', str(row.get('from_station_name'))),
                         '\n',
                         colorit('red', str(row.get('to_station_name')))]),
                # Column: '时间'
                ''.join([colorit('green', str(row.get('start_time'))),
                         '\n',
                         colorit('red', str(row.get('arrive_time')))]),
                # Column: '历时'
                self._get_time_duration(row),
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

    def export(self, options):
        """Use pretty table to perform formatting outprint.

        :options: Null string or a subset of 'dgktz'.

        """
        pt = PrettyTable()
        pt._set_field_names(self.headers)
        if options:
            for t in self.trains:
                if t[0][0].lower() in options:
                    pt.add_row(t)
        else:
            for t in self.trains:
                pt.add_row(t)
        return pt


def get_valid_date(date):
    date = re.sub(r'[/\:,]+', '', date)
    try:
        date = datetime.strptime(date, '%Y%m%d')
    except ValueError:
        print(colorit('red', '请输入正确的日期格式, 如20161001, 2016-10-1等.'))
        exit()
    diff = date - datetime.today()
    if diff.days not in range(-1, 50):
        print(colorit('red', '请输入今日起50天内的日期.'))
        exit()
    return datetime.strftime(date, '%Y-%m-%d')


def cli():
    # Parse the command-line arguments.
    arguments = docopt(__doc__)

    # Get `from` station telecode
    from_station_code = stations.get(arguments['<from>'])
    # Get `goto` station telecode
    goto_station_code = stations.get(arguments['<goto>'])
    raw_date = arguments['<date>']

    # Verify if `from` station is valid.
    if not from_station_code:
        print('你出发的站点国内貌似没有, 你来自火星吗?')
        exit()

    # Verify if `goto` station is valid.
    if not goto_station_code:
        print('你要去的站点国内貌似没有, 你要去火星吗?')
        exit()

    # Verify and get valid date.
    date = get_valid_date(raw_date)

    # Real query URL.
    url = QUERY_URL.format(date, from_station_code, goto_station_code)

    # Transform valid options to a string.
    options = ''.join(o[1] for o in arguments if o in '-d-g-k-t-z' and arguments[o])

    try:
        resp = requests.get(url, verify=False)
    except ConnectionError:
        print(colorit('red', '网络连接失败.'))
        exit()

    try:
        rows = resp.json()['data']['datas']
    except KeyError:
        print(colorit('green', '很遗憾，没有符合要求的车次'))

    trains = TrainsCollection(rows, options)

    print(trains.export(options))


if __name__ == '__main__':
    cli()
