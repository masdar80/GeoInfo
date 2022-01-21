
from django.db.models import Q
from functools import reduce

import datetime


def filter_riverdischarge_anual(riverdischarge_anuals, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            riverdischarge_anuals = riverdischarge_anuals.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            riverdischarge_anuals = riverdischarge_anuals.filter(obs_datetime__lte=_before_date)

    return riverdischarge_anuals
def filter_riverdischarge_monthly(riverdischarge_monthlys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            riverdischarge_monthlys = riverdischarge_monthlys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            riverdischarge_monthlys = riverdischarge_monthlys.filter(obs_datetime__lte=_before_date)

    return riverdischarge_monthlys
def filter_riverdischarge_daily(riverdischarge_dailys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            riverdischarge_dailys = riverdischarge_dailys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            riverdischarge_dailys = riverdischarge_dailys.filter(obs_datetime__lte=_before_date)

    return riverdischarge_dailys
def filter_riverflowmeasure(riverflowmeasures, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            riverflowmeasures = riverflowmeasures.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            riverflowmeasures = riverflowmeasures.filter(obs_datetime__lte=_before_date)

    return riverflowmeasures
def filter_surface_hq(surface_hqs, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            surface_hqs = surface_hqs.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            surface_hqs = surface_hqs.filter(obs_datetime__lte=_before_date)

    return surface_hqs
def filter_discharge_survey(discharge_surveys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            discharge_surveys = discharge_surveys.filter(year__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            discharge_surveys = discharge_surveys.filter(year__lte=_before_date)

    return discharge_surveys

def filter_sectionareasurvey(sectionareasurveys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            sectionareasurveys = sectionareasurveys.filter(datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            sectionareasurveys = sectionareasurveys.filter(datetime__lte=_before_date)

    return sectionareasurveys
def filter_sectiondata(sectiondatas, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            sectiondatas = sectiondatas.filter(sec_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            sectiondatas = sectiondatas.filter(sec_datetime__lte=_before_date)

    return sectiondatas
