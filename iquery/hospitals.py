# -*- coding: utf-8 -*-

"""
iquery.hospitals
~~~~~~~~~~~~~~~~~~~~~~

Check whether a hospital is putian series or display
all putian series hospitals in a city. The datas come
from:
    https://github.com/open-power-workgroup/Hospital
"""

from prettytable import PrettyTable
from .utils import colored, requests_get, exit_after_echo


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

        if len(self._params) == 2:
            #: User input a hospital name after city
            self._hospital = self._params[1]
        else:
            self._hospital = ''

    @property
    def putian_hospitals_in_city(self):
        hospitals = self._rows.get(self._city, None)
        if hospitals is None:
            exit_after_echo('City is not supported.')
        return iter(hospitals)

    def pretty_print(self):

        if not self._hospital:
            pt = PrettyTable()
            pt._set_field_names([self._city])
            for hospital in self.putian_hospitals_in_city:
                pt.add_row([colored.green(hospital) + '\n'])
            print(pt)

        else:
            is_putian, field_name = False, self._city + self._hospital

            for hospital in self.putian_hospitals_in_city:
                pt = PrettyTable()
                if self._hospital in hospital:
                    is_putian, field_name = True, hospital
                    pt._set_field_names([field_name])
                    pt.add_row([colored.green(str(is_putian))])
                    print(pt)


def query(params):
    """`params` is a city name or a city name + hospital name.

    CLI:

        1. query all putian hospitals in a city:

        $ iquery -p 南京
        +------+
        | 南京 |
        +------+
        |...   |
        +------+
        |...   |
        +------+
        ...


        2. query if the hospital in the city is putian
           series, you can only input hospital's short name:

        $ iquery -p 南京 曙光
        +------------+
        |南京曙光医院|
        +------------+
        |    True    |
        +------------+

    """

    r = requests_get(QUERY_URL)

    return HospitalCollection(r.json(), params)
