# -*- coding: utf-8 -*-

"""
iquery.lottery
~~~~~~~~~~~~~

lottery query from `http://baidu.lecai.com/`.
"""

from pyquery import PyQuery as pq
from prettytable import PrettyTable
from .utils import colored, requests_get


__all__ = ['query']

# 目前基于百度乐彩的开奖信息
QUERY_URL = 'http://baidu.lecai.com/lottery/draw/?agentId=5571'
QUERY_DETAIL_URL = 'http://baidu.lecai.com/lottery/draw/list/{id}'
# ERR MSG
# LOTTERY_NOT_FOUND = 'Sorry, not found.'


class LotteryPage(object):

    """基于百度乐彩 """

    header = '编号 彩种 期号 开奖时间 开奖号码 奖池滚存(元)'.split()
    need_to_show = u'双色球 七乐彩 大乐透 七星彩'.split()

    def __init__(self, lottery_url):
        self.url = lottery_url
        self.html_content = requests_get(self.url).text

        #: pyquery object
        d = pq(self.html_content)
        self._rows = d('table.kj_tab tr')

    def __repr__(self):
        return '<LotteryPage url={!r}>'.format(self.url)

    @property
    def lotteries(self):
        """用于生成所有彩种最近开奖信息"""
        for idx, row in enumerate(self._rows):
            i = pq(row)
            cz = i('td:eq(0)').text().strip()
            if cz in self.need_to_show:
                qh = i('td:eq(1)').text().strip()
                kjsj = i('td:eq(2)').text().strip()
                hm_r = colored.red(i('td:eq(3) span.ball_1').text().strip())
                hm_g = colored.green(i('td:eq(3) span.ball_2').text().strip())
                kjhm = ' '.join([hm_r, hm_g])
                jcgc = i('td:eq(4)').text().strip()

                lottery = [idx, cz, qh, kjsj, kjhm, jcgc]
                yield lottery

    def _get_lottery_detail_by_id(self, id):
        """
        相应彩种历史信息生成
        百度详细信息页有两种结构，需要分开处理
        """
        header = '编号 期号 开奖日期 开奖号码'.split()
        pt = PrettyTable()
        pt._set_field_names(header)

        url = QUERY_DETAIL_URL.format(id=id)
        import requests
        content = requests.get(url).text
        d = pq(content)
        if d('table.historylist'):
            # 输出彩种
            info = d('div.historyHd1 h2').text()
            print(info)
            # 输出table
            rows = d('table.historylist>tbody>tr')
            for idx, row in enumerate(rows):
                i = pq(row)
                qh = i('td:eq(0)').text().strip()
                kjrq = i('td:eq(1)').text().strip()
                hm_r = colored.red(i('td:eq(2) td.redBalls').text().strip())
                hm_g = colored.green(i('td:eq(2) td.blueBalls').text().strip())
                kjhm = ' '.join([hm_r, hm_g])
                item = [idx + 1, qh, kjrq, kjhm]
                pt.add_row(item)
            print(pt)
        elif d('table#draw_list'):
            # 输出彩种
            info = d('div.cpinfo>div.title').text()
            print(info)
            # 输出table
            rows = d('table#draw_list>tbody>tr')
            for idx, row in enumerate(rows):
                i = pq(row)
                qh = i('td.td2').text().strip()
                kjrq = i('td.td1').text().strip()
                hm_r = colored.red(i('td.td3 span.ball_1').text().strip())
                hm_g = colored.green(i('td.td3 span.ball_2').text().strip())
                kjhm = ' '.join([hm_r, hm_g])
                item = [idx + 1, qh, kjrq, kjhm]
                pt.add_row(item)
            print(pt)
        else:
            print('请联系作者')

    def get_lottery_detail(self, num):
        item = self._rows[num]
        i = pq(item)
        cz = i('td:eq(0)').text().strip()
        if cz in self.need_to_show:
            url = i('td:eq(0)>a').attr('href').strip()
            lottery_id = int(url.split('/')[-1])
            self._get_lottery_detail_by_id(lottery_id)
        else:
            print('Invalid number.请按编号栏输入编号')

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        # align left
        pt.align["开奖号码"] = "l"
        pt.align["奖池滚存(元)"] = "l"
        for item in self.lotteries:
            pt.add_row(item)
        print(pt)

        print('输入编号获取相应彩种往期中奖号码:')
        while True:
            raw = input('>> ')
            if raw in ('q', 'quit'):
                exit()
            try:
                num = int(raw)
            except ValueError:
                print('Invalid number.请按编号栏输入编号')
                continue

            if (num - 1) in range(len(self._rows)):
                self.get_lottery_detail(num)
            else:
                print('Invalid number.')


def query():
    """Query lottery infomation from baidu lecai."""

    return LotteryPage(QUERY_URL)
