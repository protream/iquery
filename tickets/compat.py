# -*- coding: utf-8 -*-
"""
    tickets._compat
    ~~~~~~~~~~~~~~~

    Compatibility for Python2 and Python3.
"""
import sys


_ver = sys.version_info

#: Py2.*?
is_py2 = (_ver[0] == 2)

#: Py3.*?
is_py3 = (_ver[0] == 3)

if is_py2:
    unicode_type = unicode
    bytes_type = str
elif is_py3:
    unicode_type = str
    bytes_type = bytes


def to_unicode(value, encoding='utf-8'):
    if isinstance(value, unicode_type):
        return value

    if isinstance(value, bytes_type):
        return unicode_type(value, encoding=encoding)

    if isinstance(value, int):
        return unicode_type(str(value))

    return value
