# -*- coding: utf-8 -*-

"""
iquery.putian_hospitals
~~~~~~~~~~~~~~~~~~~~~~

Check whether a hospital is putian series or display
all putian series hospitals in a city. The datas come
from:
    https://github.com/open-power-workgroup/Hospital
"""

import requests
import itertools
from .utils import args, colored, exit_after_echo
from prettytable import PrettyTable
from requests.exceptions import ConnectionError, Timeout


__all__ = ['query']


QUERY_URL = ('https://raw.githubusercontent.com/'
             'open-power-workgroup/Hospital/master/'
             'resource/API_resource/hospital_list.json')


class HospitalCollection(object):

    """Putian hospitals data sets."""

    def __init__(self, rows, params):
        self._rows = rows

        self._params = params

        #: All supported cities.
        self._citys = rows.keys()

    def pretty_print(self):

        pt = PrettyTable()

        l = len(self._params)

        city = self._params[0]
        if city not in self._citys:
            exit_after_echo('City is not supported.')
        hospitals = self._rows.get(city)

        if l == 1:
            pt._set_field_names([city])
            for idx, h in enumerate(hospitals):
                color = colored.red
                pt.add_row([color(h) + '\n'])
            print(pt)
            return

        if l == 2:
            hospital = self._params[1]
            field_name = city + hospital
            is_putian = False
            for h in hospitals:
                if hospital in h:
                    is_putian = True
                    field_name = h
                    break
            pt._set_field_names([field_name])
            color = colored.red if is_putian else colored.green
            pt.add_row([color(str(is_putian))])
            print(pt)
            return


def query(params):
    """`params` is a `hospital` name  or a `city` name."""

    try:
        r = requests.get(QUERY_URL)
    except ConnectionError:
        exit_after_echo('Network connection failed.')

    return HospitalCollection(r.json(), params)
