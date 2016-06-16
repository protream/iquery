# -*- coding: utf-8 -*-

"""
    tickets.core
    ~~~~~~~~~~~~

    tickets command-line interface.
"""

import sys
import requests
import colorama
from .utils import args, exit_after_echo
from .showes import ShowTicketsQuery
from .trains import TrainTicketsQuery


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


def show_usage():
    """
Usage:
    tickets [-dgktz] <from> <to> <date>
    tickets <city> <show-type> <within-days>

You can go to `tickets -h` for more details.
    """
    pass


def cli():
    """Tickets query via the command line.

Usage:
    tickets [-dgktz] <from> <to> <date>
    tickets <city> <show> [<days>]

 Arguments:
    from             出发站
    to               到达站
    date             查询日期

    city             查询城市
    show             演出的类型
    days             查询近(几)天内的演出, 若省略, 默认15


Options:
    -h, --help       显示该帮助菜单.
    -d               动车
    -g               高铁
    -k               快速
    -t               特快
    -z               直达

Show:
    演唱会 音乐会 比赛 话剧 歌剧 舞蹈 戏曲 相声 音乐剧 歌舞剧 儿童剧 杂技 马戏 魔术

Examples:
    tickets 南京 北京 201671
    tickets -k  南京南 上海 2016-7-1
    tickets -dg 上海虹桥 北京西 2016/7/1

    tickets 上海 演唱会
    tickets 北京 比赛 7
    """

    colorama.init()

    if args.is_asking_for_help:
        exit_after_echo(cli.__doc__, color=None)

    elif args.is_querying_show:
        q = ShowTicketsQuery(*args.as_show_query_params)

    elif args.is_querying_train:
        q = TrainTicketsQuery(*args.as_train_query_params)

    else:
        exit_after_echo(show_usage.__doc__, color=None)

    q.query().pretty_print()
