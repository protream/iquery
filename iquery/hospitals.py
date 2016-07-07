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
        self._city = self._params[0]

    @property
    def putian_hospitals_in_city(self):
        hospitals = self._rows.get(self._city, None)
        if hospitals is None:
            exit_after_echo('City is not supported.')
        return iter(hospitals)

    def pretty_print(self):

        pt = PrettyTable([self._city])

        l = len(self._params)

        if l == 1:
            pt._set_field_names([self._city])
            for hospital in self.putian_hospitals_in_city:
                color = colored.red
                pt.add_row([color(hospital) + '\n'])
            print(pt)

        if l == 2:
            # User input hospital name
            h = self._params[1]

            is_putian, field_name = False, self._city + h

            for hospital in self.putian_hospitals_in_city:
                if h in hospital:
                    is_putian, field_name = True, hospital
                    break

            pt._set_field_names([field_name])
            color = colored.red if is_putian else colored.green
            pt.add_row([color(str(is_putian))])
            print(pt)


def query(params):
    """`params` is a `hospital` name  or a `city` name."""

    try:
        r = requests.get(QUERY_URL)
    except ConnectionError:
        exit_after_echo('Network connection failed.')

    return HospitalCollection(r.json(), params)
