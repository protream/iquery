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

QUERY_URL = 'http://baidu.lecai.com/lottery/draw/?agentId=5571'
# ERR MSG
# LOTTERY_NOT_FOUND = 'Sorry, not found.'


class LotteryPage(object):

    """The query lottery's page on baidu lecai. """

    header = '彩种 期号 开奖时间 开奖号码 奖池滚存(元)'.split()
    need_to_show = u'双色球 七乐彩 大乐透 七星彩'.split()

    def __init__(self, lottery_url):
        self.url = lottery_url
        self.html_content = requests_get(self.url).text

        #: pyquery object
        d = pq(self.html_content)
        self._raws = d('table.kj_tab tr')

    def __repr__(self):
        return '<LotteryPage url={!r}>'.format(self.url)

    @property
    def lotteries(self):
        for _, raw in enumerate(self._raws):
            i = pq(raw)
            cz = i('td:eq(0)').text().strip()
            if cz in self.need_to_show:
                qh = i('td:eq(1)').text().strip()
                kjsj = i('td:eq(2)').text().strip()
                hm_r = colored.red(i('td:eq(3) span.ball_1').text().strip())
                hm_g = colored.green(i('td:eq(3) span.ball_2').text().strip())
                kjhm = ' '.join([hm_r, hm_g])
                jcgc = i('td:eq(4)').text().strip()

                lottery = [cz, qh, kjsj, kjhm, jcgc]
                yield lottery

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        # align left
        pt.align["开奖号码"] = "l"
        pt.align["奖池滚存(元)"] = "l"
        for item in self.lotteries:
            pt.add_row(item)
        print(pt)


def query():
    """Query hot movies infomation from baidu lecai."""

    return LotteryPage(QUERY_URL)
