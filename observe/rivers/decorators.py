from django.core.exceptions import PermissionDenied
from observe.rivers.models import XY_River,riverdischarge_anual,riverdischarge_monthly,riverdischarge_daily,riverflowmeasure\
    ,surface_hq,discharge_survey,sectionareasurvey,sectiondata
from django.shortcuts import render, redirect, get_object_or_404

def user_is_riverdischarge_anual_author(function):
    def wrap(request, id_field,id):
        riverdischarge_anual_new = get_object_or_404(riverdischarge_anual,pk=id)
        if riverdischarge_anual_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_riverdischarge_monthly_author(function):
    def wrap(request, id_field,id):
        riverdischarge_monthly_new = get_object_or_404(riverdischarge_monthly,pk=id)
        if riverdischarge_monthly_new.created_by == request.user:
            request.temp_daily = riverdischarge_monthly_new
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_riverdischarge_daily_author(function):
    def wrap(request, id_field,id):
        riverdischarge_daily_new = get_object_or_404(riverdischarge_daily,pk=id)
        if riverdischarge_daily_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_riverflowmeasure_author(function):
    def wrap(request, id_field,id):
        riverflowmeasure_new = get_object_or_404(riverflowmeasure,pk=id)
        if riverflowmeasure_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_surface_hq_author(function):
    def wrap(request, id_field,id):
        surface_hq_new = get_object_or_404(surface_hq,pk=id)
        if surface_hq_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_discharge_survey_author(function):
    def wrap(request, id_field,id):
        discharge_survey_new = get_object_or_404(discharge_survey,pk=id)
        if discharge_survey_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_sectionareasurvey_author(function):
    def wrap(request, id_field,id):
        sectionareasurvey_new = get_object_or_404(sectionareasurvey,pk=id)
        if sectionareasurvey_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_sectiondata_author(function):
    def wrap(request, id_field,id):
        sectiondata_new = get_object_or_404(sectiondata,pk=id)
        if sectiondata_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
