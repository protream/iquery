tickets
===========================================================

.. image:: https://img.shields.io/pypi/dm/tickets.svg
        :target: https://pypi.python.org/pypi/tickets

tickets提供基于命令行的火车票、演出及热映电影的信息查询.


Usage
-----

火车查询
````````

命令行下输入:

::

    $ tickets 上海虹桥 北京 617

你将获得本年6-17从上海虹桥到北京的火车票信息:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/ticksts-train.png

...

当然你也可以指定火车的类型和输入完整的查询日期, 比如:

::

    $ tickets -dg 上海 北京 20160617

只查询动车和高铁.

演出查询
````````

命令行下输入：

::

    $ tickets 南京 音乐会

你将获得未来15天内在南京的音乐会信息：

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/tickets-show.png

当然, 你也可以指定查询未来多少天:

::

    $ tickets 上海 演唱会 7

只查询一周内的信息.


电影查询
````````

命令行下输入:

::

    $ tickets -m 或者 $ tickets 电影

你将获得当前热映的电影信息:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/tickets_movies.png

输出电影信息后，你可以输入你感兴趣的电影编号查看电影简介, 比如输入2获得独立日的简介:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/tickets_movie_summary.png

输入q或quit退出.

Install
-------

tickets使用Python3编写，请使用pip3安装:

::

    $ pip3 install tickets

或者下载源码安装:

::

    $ git clone https://github.com/protream/tickets

然后到下载目录:

::

    $ ./setup.py install

Help
----

::

    Usage:
        tickets (-m|电影)
        tickets <city> <show> [<days>]
        tickets [-dgktz] <from> <to> <date>

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

        -m               查询当前热映的电影

    Show:
        演唱会 音乐会 比赛 话剧 歌剧 舞蹈 戏曲 相声 音乐剧 歌舞剧 儿童剧 杂技 马戏 魔术

    Examples:
        tickets -m
        tickets 电影

        tickets 上海 演唱会
        tickets 北京 比赛 7

        tickets 南京 北京 201671
        tickets -k  南京南 上海 2016-7-1
        tickets -dg 上海虹桥 北京西 2016/7/1



Notes
-----

- 火车票查询最多查询未来50天内.

- 确保你的查询日期不要有歧义, 比如111可以是1.11也可以是11.1, 默认解析为11.1
