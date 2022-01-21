
from django.db.models import Q
from functools import reduce

import datetime


def filter_springdischarge_anual(springdischarge_anuals, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            springdischarge_anuals = springdischarge_anuals.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            springdischarge_anuals = springdischarge_anuals.filter(obs_datetime__lte=_before_date)

    return springdischarge_anuals
def filter_springdischarge_avg_anual(springdischarge_avg_anuals, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            springdischarge_avg_anuals = springdischarge_avg_anuals.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            springdischarge_avg_anuals = springdischarge_avg_anuals.filter(obs_datetime__lte=_before_date)

    return springdischarge_avg_anuals
def filter_springdischarge_monthly(springdischarge_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            springdischarge_monthlys = springdischarge_monthlys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            springdischarge_monthlys = springdischarge_monthlys.filter(obs_datetime__lte=_before_date)

    return springdischarge_monthlys
def filter_springdischarge_avg_monthly(springdischarge_avg_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['month_after'] != '':
            after_date = paramDict['month_after']
            # _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            springdischarge_avg_monthlys = springdischarge_avg_monthlys.filter(month__gte=after_date)

        if paramDict['month_before'] != '':
            before_date = paramDict['month_before']
            # _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            springdischarge_avg_monthlys = springdischarge_avg_monthlys.filter(month__lte=before_date)

    return springdischarge_avg_monthlys
def filter_springdischarge_daily(springdischarge_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            springdischarge_dailys = springdischarge_dailys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            springdischarge_dailys = springdischarge_dailys.filter(obs_datetime__lte=_before_date)

    return springdischarge_dailys
