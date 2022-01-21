
from django.db.models import Q
from functools import reduce

import datetime


def filter_lithologging(lithologgings, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            lithologgings = lithologgings.filter(depth_from__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            lithologgings = lithologgings.filter(depth_from__lte=_before_date)

    return lithologgings
# def filter_loggingdata(loggingdatas, paramDict):
#     params = paramDict.keys()
#     if any(x != '' for x in paramDict.values()):
#         if paramDict['obs_datetime_after'] != '':
#             after_date = paramDict['obs_datetime_after']
#             _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
#             loggingdatas = loggingdatas.filter(depth_from__gte=_after_date)
#
#         if paramDict['obs_datetime_before'] != '':
#             before_date = paramDict['obs_datetime_before']
#             _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
#             loggingdatas = loggingdatas.filter(depth_from__lte=_before_date)
#
#     return loggingdatas
def filter_drilling(drillings, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            drillings = drillings.filter(drilling_from__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            drillings = drillings.filter(drilling_from__lte=_before_date)

    return drillings
def filter_casing(casings, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            casings = casings.filter(casing_from__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            casings = casings.filter(casing_from__lte=_before_date)

    return casings
def filter_packing(packings, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            packings = packings.filter(packing_from__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            packings = packings.filter(packing_from__lte=_before_date)

    return packings
def filter_welllogging(wellloggings, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            wellloggings = wellloggings.filter(log_from__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            wellloggings = wellloggings.filter(log_from__lte=_before_date)

    return wellloggings
def filter_auto_groundwater(auto_groundwaters, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            auto_groundwaters = auto_groundwaters.filter(obs_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            auto_groundwaters = auto_groundwaters.filter(obs_date__lte=_before_date)

    return auto_groundwaters
def filter_welltoplevel(welltoplevels, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            welltoplevels = welltoplevels.filter(meas_date__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            welltoplevels = welltoplevels.filter(meas_date__lte=_before_date)

    return welltoplevels
def filter_wells_quality(wells_qualitys, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            wells_qualitys = wells_qualitys.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            wells_qualitys = wells_qualitys.filter(obs_datetime__lte=_before_date)

    return wells_qualitys
def filter_groundwaterlevel_manual(groundwaterlevel_manuals, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            groundwaterlevel_manuals = groundwaterlevel_manuals.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            groundwaterlevel_manuals = groundwaterlevel_manuals.filter(obs_datetime__lte=_before_date)

    return groundwaterlevel_manuals
def filter_groundwaterlevel(groundwaterlevels, paramDict):
    params = paramDict.keys()
    if any(x != '' for x in paramDict.values()):
        if paramDict['obs_datetime_after'] != '':
            after_date = paramDict['obs_datetime_after']
            _after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
            groundwaterlevels = groundwaterlevels.filter(obs_datetime__gte=_after_date)

        if paramDict['obs_datetime_before'] != '':
            before_date = paramDict['obs_datetime_before']
            _before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            groundwaterlevels = groundwaterlevels.filter(obs_datetime__lte=_before_date)

    return groundwaterlevels