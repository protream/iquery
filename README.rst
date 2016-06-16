tickets
===========================================================
tickets enable you variable tickets via command line, type:

::

    $ tickets -dt 上海 北京 20160615

in command line, get train tickets from `上海` to `北京` in 2016-06-15:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/tickets.png

or, type

::

    $ tickets 上海 演唱会

you will get the show within `15` days:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/tickets-2.png

You can specify within how many days, like:

::

    $ tickets 上海 演唱会 7

to query 7 days in the future.


Install
-------

::

    $ pip3 install tickets

or

::

    $ git clone https://github.com/protream/tickets

then go to `tickets` dir,

::

    $ ./setup.py install

Usage
-----

::

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

Notes
-----

- In consideration of `tickets` is just a tool, not lib, so not much necessary to suport Pyhton2 anymore.

- Train query date surport max 50 days offset today, less or more will be considered as a invalid date.

- If you don't use delimiter, make sure your date is not ambiguous. e.g. By 2016115 you mean 2016-1-15 or 2016-11-5 ? By default, it parsed to 2016-11-5.
