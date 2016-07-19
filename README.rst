iquery
===========================================================

iquery提供基于命令行各种信息查询.


Usage
-----

火车查询
````````

命令行下输入:

::

    $ iquery 上海虹桥 北京 617

你将获得本年6-17从上海虹桥到北京的火车票信息:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/ticksts-train.png

...

当然你也可以指定火车的类型和输入完整的查询日期, 比如:

::

    $ iquery -dg 上海 北京 20160617

只查询动车和高铁.

演出查询
````````

命令行下输入：

::

    $ iquery 南京 音乐会

你将获得未来15天内在南京的音乐会信息：

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/iquery-show.png

当然, 你也可以指定查询未来多少天:

::

    $ iquery 上海 演唱会 7

只查询一周内的信息.


电影查询
````````

命令行下输入:

::

    $ iquery -m 或者 $ iquery 电影

你将获得当前热映的电影信息:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/iquery_movies.png

...

输出电影信息后，你可以输入你感兴趣的电影编号查看电影简介, 比如输入2获得独立日的简介:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/iquery_movie_summary.png

输入q或quit退出.


莆田系医院查询
``````````````

提供俩个接口,

1. -p + 城市名, 如：

::

    $ iquery -p 北京

获取该城市所有莆田系医院的一个列表.

::

    +------------+
    |     北京    |
    +------------+
    | 北京XXX医院 |
    | 北京XXX医院 |
    | ...        |
    +------------+


2. -p + 城市名 + 医院名, 假设 ``曙光`` 代表 ``上海曙光男科医院`` (我不知道是否真有这个医院), 只需输入:

::

    $ iquery -p 上海 曙光

就可以判断该医院是否是莆田系, 当然你输入医院全名也是可以的, 返回 ``True`` 或 ``False``:

::

    +---------------+
    | 上海曙光男科医院 |
    +---------------+
    |       True    |
    +---------------+

数据来源: https://github.com/open-power-workgroup/Hospital

Install
-------

iquery使用Python3编写，请使用pip3安装:

::

    $ pip3 install iquery

或者下载源码安装:

::

    $ git clone https://github.com/protream/iquery

然后到下载目录:

::

    $ ./setup.py install

Help
----

::

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


    Go to https://github.com/protream/iquery for usage examples.

Notes
-----

- 火车票查询最多查询未来50天内.

- 确保你的查询日期不要有歧义, 比如111可以是1.11也可以是11.1, 默认解析为11.1
