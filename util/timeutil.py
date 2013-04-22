import calendar
from datetime import datetime, timedelta


def utcnow(**offset):
    '''offset is passed to timedelta'''
    return datetime.utcnow() + timedelta(**offset)


def utc_asint(utc):
    return calendar.timegm(utc.utctimetuple())
