# from ..models import riverdischarge_daily
from django.db.models import Q
from functools import reduce

import datetime


def filter_evaporation_daily(evaporation_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            evaporation_dailys = evaporation_dailys.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            evaporation_dailys = evaporation_dailys.filter(obs_date__lte=_before_date)

    return evaporation_dailys
def filter_snowdepth(snowdepths, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            snowdepths = snowdepths.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            snowdepths = snowdepths.filter(obs_datetime__lte=_before_date)

    return snowdepths
def filter_snowfall(snowfalls, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            snowfalls = snowfalls.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            snowfalls = snowfalls.filter(obs_date__lte=_before_date)

    return snowfalls
def filter_evaporation_monthly(evaporation_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            evaporation_monthlys = evaporation_monthlys.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            evaporation_monthlys = evaporation_monthlys.filter(obs_date__lte=_before_date)

    return evaporation_monthlys
def filter_humidity_daily(humidity_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            humidity_dailys = humidity_dailys.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            humidity_dailys = humidity_dailys.filter(obs_date__lte=_before_date)

    return humidity_dailys
def filter_temperature_daily(temperature_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            temperature_dailys = temperature_dailys.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            temperature_dailys = temperature_dailys.filter(obs_date__lte=_before_date)

    return temperature_dailys
def filter_precipitation_daily(precipitation_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            precipitation_dailys = precipitation_dailys.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            precipitation_dailys = precipitation_dailys.filter(obs_date__lte=_before_date)

    return precipitation_dailys
def filter_sunshine_daily(sunshine_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            sunshine_dailys = sunshine_dailys.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            sunshine_dailys = sunshine_dailys.filter(obs_date__lte=_before_date)

    return sunshine_dailys

def filter_humidity_monthly(humidity_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            humidity_monthlys = humidity_monthlys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            humidity_monthlys = humidity_monthlys.filter(obs_datetime__lte=_before_date)

    return humidity_monthlys
def filter_airpressure(airpressures, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            airpressures = airpressures.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            airpressures = airpressures.filter(obs_datetime__lte=_before_date)

    return airpressures
def filter_temperature_monthly(temperature_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            temperature_monthlys = temperature_monthlys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            temperature_monthlys = temperature_monthlys.filter(obs_datetime__lte=_before_date)

    return temperature_monthlys
def filter_precipitation_monthly(precipitation_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            precipitation_monthlys = precipitation_monthlys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            precipitation_monthlys = precipitation_monthlys.filter(obs_datetime__lte=_before_date)

    return precipitation_monthlys
def filter_wind_daily(wind_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            wind_dailys = wind_dailys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            wind_dailys = wind_dailys.filter(obs_datetime__lte=_before_date)

    return wind_dailys
def filter_wind_monthly(wind_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            wind_monthlys = wind_monthlys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            wind_monthlys = wind_monthlys.filter(obs_datetime__lte=_before_date)

    return wind_monthlys

def filter_precipitation_annual(precipitation_annuals, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['year_after'] != '':
            after_date = paramDict['year_after']
            # _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            precipitation_annuals = precipitation_annuals.filter(year__gte=after_date)

        if paramDict['year_before'] != '':
            before_date = paramDict['year_before']
            # _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            precipitation_annuals = precipitation_annuals.filter(year__lte=before_date)

    return precipitation_annuals

def filter_date(tablemodel, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            tablemodel = tablemodel.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            tablemodel = tablemodel.filter(obs_datetime__lte=_before_date)
    return tablemodel


def filter_waterpoints(Waterpoints , paramDict):
    params = paramDict.keys()

    # data filtering
    if any(x != '' for x in paramDict.values()):

        # filters records that contain any of the following keywords
        if paramDict['keywords'] != '':
            kws = paramDict['keywords'].split()
            q_lookups = [Q(mohafaza__icontains=kw) for kw in kws] + \
                        [Q(montika__icontains=kw) for kw in kws] + \
                        [Q(type__icontains=kw) for kw in kws] + \
                        [Q(id_field__icontains=kw) for kw in kws] + \
                        [Q(village__icontains=kw) for kw in kws] + \
                        [Q(sub_baisn__icontains=kw) for kw in kws] + \
                        [Q(sitename_e__icontains=kw) for kw in kws]
            filters = Q()
            filters |= reduce(lambda x, y: x | y, q_lookups)
            Waterpoints = Waterpoints.filter(filters)

    return Waterpoints
