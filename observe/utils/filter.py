# from ..models import riverdischarge_daily
from django.db.models import Q
from functools import reduce

import datetime


def filter_riverdischarge_daily(riverdischarge_daily, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            riverdischarge_dailys = riverdischarge_daily.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            riverdischarge_dailys = riverdischarge_daily.filter(obs_datetime__lte=_before_date)

    return riverdischarge_dailys

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
