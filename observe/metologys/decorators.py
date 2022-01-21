from django.core.exceptions import PermissionDenied
from observe.metologys.models import XY_Metology,airpressure,evaporation_daily,evaporation_monthly,temperature_daily\
    ,temperature_monthly,precipitation_annual,precipitation_daily,precipitation_monthly,wind_monthly,wind_daily,\
    snowfall,snowdepth,humidity_monthly,humidity_daily,sunshine_daily
from django.shortcuts import render, redirect, get_object_or_404

def user_is_air_pressure_author(function):
    def wrap(request, id_field,id):
        air_pressure = get_object_or_404(airpressure,pk=id)
        if air_pressure.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_temp_daily_author(function):
    def wrap(request, id_field,id):
        temp_daily = get_object_or_404(temperature_daily,pk=id)
        if temp_daily.created_by == request.user:
            request.temp_daily = temp_daily
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_temp_monthly_author(function):
    def wrap(request, id_field,id):
        temp_monthly = get_object_or_404(temperature_monthly,pk=id)
        if temp_monthly.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_ed_author(function):
    def wrap(request, id_field,id):
        evap_daily = get_object_or_404(evaporation_daily,pk=id)
        if evap_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_em_author(function):
    def wrap(request, id_field,id):
        evap_monthly = get_object_or_404(evaporation_monthly,pk=id)
        if evap_monthly.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_td_author(function):
    def wrap(request, id_field,id):
        temp_daily = get_object_or_404(temperature_daily,pk=id)
        if temp_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_tm_author(function):
    def wrap(request, id_field,id):
        temp_monthly = get_object_or_404(temperature_monthly,pk=id)
        if temp_monthly.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_pd_author(function):
    def wrap(request, id_field,id):
        precp_daily = get_object_or_404(precipitation_daily,pk=id)
        if precp_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_pm_author(function):
    def wrap(request, id_field,id):
        precp_monthly = get_object_or_404(precipitation_monthly,pk=id)
        if precp_monthly.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_pa_author(function):
    def wrap(request, id_field,id):
        precp_anuall = get_object_or_404(precipitation_annual,pk=id)
        if precp_anuall.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_wd_author(function):
    def wrap(request, id_field,id):
        win_daily = get_object_or_404(wind_daily,pk=id)
        if win_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_wm_author(function):
    def wrap(request, id_field,id):
        win_monthly = get_object_or_404(wind_monthly,pk=id)
        if win_monthly.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_hd_author(function):
    def wrap(request, id_field,id):
        hum_daily = get_object_or_404(humidity_daily,pk=id)
        if hum_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_hm_author(function):
    def wrap(request, id_field,id):
        hum_monthly = get_object_or_404(humidity_monthly,pk=id)
        if hum_monthly.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_sd_author(function):
    def wrap(request, id_field,id):
        sunsh_daily = get_object_or_404(sunshine_daily,pk=id)
        if sunsh_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_snowfall_author(function):
    def wrap(request, id_field,id):
        snowfall_daily = get_object_or_404(snowfall,pk=id)
        if snowfall_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_snowdepth_author(function):
    def wrap(request, id_field,id):
        snowdepth_daily = get_object_or_404(snowdepth,pk=id)
        if snowdepth_daily.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap