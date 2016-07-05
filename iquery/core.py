# -*- coding: utf-8 -*-

"""
iquery.core
~~~~~~~~~~~~

The program entrance.
"""

from .utils import args, exit_after_echo


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
    """Usage:
    iquery (-m|电影)
    iquery -p <city>
    iquery -p <city> <hospital>
    iquery <city> <show> [<days>]
    iquery [-dgktz] <from> <to> <date>

Go to `tickets -h` for more details.
"""
    pass


def cli():
    """Various information query via command line.

Usage:
    iquery (-m|电影)
    iquery -p <city>
    iquery -p <city> <hospital>
    iquery <city> <show> [<days>]
    iquery [-dgktz] <from> <to> <date>

Arguments:
    from             出发站
    to               到达站
    date             查询日期

    city             查询城市
    show             演出的类型
    days             查询近(几)天内的演出, 若省略, 默认15

    city             城市名,加在-p后查询该城市所有莆田医院
    hospital         医院名,加在city后检查该医院是否是莆田系


Options:
    -h, --help       显示该帮助菜单.

    -dgktz           动车,高铁,快速,特快,直达

    -m               热映电影查询
    -p               莆田系医院查询

Show:
    演唱会 音乐会 音乐剧 歌舞剧 儿童剧 话剧
    歌剧 比赛 舞蹈 戏曲 相声 杂技 马戏 魔术


Go to https://github.com/protream/tickets for usage examples.
"""

    if args.is_asking_for_help:
        exit_after_echo(cli.__doc__, color=None)

    elif args.is_querying_movie:
        from .movies import query
        result = query()

    elif args.is_querying_show:
        from .showes import query
        result = query(args.as_show_query_params)

    elif args.is_querying_putian_hospital:
        from .hospitals import query
        result = query(args.as_hospital_query_params)

    elif args.is_querying_train:
        from .trains import query
        result = query(args.as_train_query_params)

    else:
        exit_after_echo(show_usage.__doc__, color=None)

    result.pretty_print()
