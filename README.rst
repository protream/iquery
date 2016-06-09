tickets
===========================================================
tickets enable you query train tickets via command line, type:

::

    $ tickets -dt 上海 北京 20160615

in command line, get:

.. image:: http://7xqdxb.com1.z0.glb.clouddn.com/tickets.png


Install
-------

::

    pip install tickets

Usage
-----

::

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

Notes
-----

- Worked with py2 and py3
