iquery
===========================================================

TODOs
-------
这个项目有段时间没有更新了，现在有一些新的想法，记录在这，也欢迎大家贡献代码：

- [ ] 为了可拓展性，改用子命令的形式，比如查火车票，iquery train-tickets ..., iquery t/tr/tt ... 应该也可以查, 取决于有没有其它 t 开头的子命令，使用模糊匹配技术
- [ ] 部分功能已经失效，需要检查更新代码
- [ ] 天气查询，集成 https://github.com/chubin/wttr.in
- [ ] Github 热门项目查询，github trends
- [ ] 测试用例, CI
- [ ] 提交到 Homebrew
- [ ] Windows 兼容性
- [ ] Alfred 插件



iquery提供基于命令行各种信息查询.

![](https://raw.githubusercontent.com/protream/iquery/master/screenshot/iquery.gif)


Usage
-----

## 火车余票查询

```
    $ iquery 南京 上海 910
    $ iquery -d 上海 北京 20160617
```

第二种方式中指定了动车类型, 并输入完整的日期, 也是可以的.

## 近期演出查询

```
    $ iquery 南京 演唱会
    $ iquery 上海 音乐会 30
```

默认查询15天内的演出, 你可以向第二种方式一样指定多少天.

## 热映电影查询

```
    $ iquery -m
```

你将获得当前热映的电影信息, 输出电影信息后，你可以输入你感兴趣的电影编号查看电影简介, 输入q或quit退出.


## 莆田系医院查询

```
    $ iquery -p 北京
    $ iquery -p 上海 长江
```

第一种方式查询一个城市内的所有莆田系医院, 第二种可以指定医院名称, 返回``True``表示该医院是莆田系.

数据来源: https://github.com/open-power-workgroup/Hospital

## 歌词查询

```
    $ iquery -l 演员
    $ iquery -l 演员 薛之谦
```

第二种针对歌名重复的情况, 你可以在后面追加歌手姓名.

## 彩票信息查询

```
    $ iquery -c
```

Install
-------

iquery使用Python3编写，请使用pip3安装:

```
    $ pip3 install iquery
```

或者下载源码安装:

```
    $ git clone https://github.com/protream/iquery
```

然后到下载目录:

```
    $ ./setup.py install
```

Help
----

```
    Usage:
        iquery (-c|彩票)
        iquery (-m|电影)
        iquery -p <city>
        iquery -l song [singer]
        iquery -p <city> <hospital>
        iquery <city> <show> [days]
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
        -l               歌词查询
        -c               彩票查询

    Show:
        演唱会 音乐会 音乐剧 歌舞剧 儿童剧 话剧
        歌剧 比赛 舞蹈 戏曲 相声 杂技 马戏 魔术


    Go to https://github.com/protream/iquery for usage examples.
```

Notes
-----

- 火车票查询最多查询未来50天内.

- 确保你的查询日期不要有歧义, 比如111可以是1.11也可以是11.1, 默认解析为11.1
