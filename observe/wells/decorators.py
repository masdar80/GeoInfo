from django.core.exceptions import PermissionDenied
from observe.wells.models import XY_Well,groundwaterlevel,groundwaterlevel_manual,wells_quality,welltoplevel\
    ,auto_groundwater,welllogging,lithologging,loggingdata,log_plot,drilling,casing,packing
from django.shortcuts import render, redirect, get_object_or_404

def user_is_groundwaterlevel_author(function):
    def wrap(request, id_field,id):
        gwl = get_object_or_404(groundwaterlevel,pk=id)
        if gwl.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_groundwaterlevel_manual_author(function):
    def wrap(request, id_field,id):
        gwlm = get_object_or_404(groundwaterlevel_manual,pk=id)
        if gwlm.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_wells_quality_author(function):
    def wrap(request, id_field,id):
        wq = get_object_or_404(wells_quality,pk=id)
        if wq.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_welltoplevel_author(function):
    def wrap(request, id_field,id):
        wt = get_object_or_404(welltoplevel,pk=id)
        if wt.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_auto_groundwater_author(function):
    def wrap(request, id_field,id):
        agw = get_object_or_404(auto_groundwater,pk=id)
        if agw.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_welllogging_author(function):
    def wrap(request, id_field,id):
        wl = get_object_or_404(welllogging,pk=id)
        if wl.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_lithologging_author(function):
    def wrap(request, id_field,id):
        ll = get_object_or_404(lithologging,pk=id)
        if ll.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_loggingdata_author(function):
    def wrap(request, id_field,id):
        ld = get_object_or_404(loggingdata,pk=id)
        if ld.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_log_plot_author(function):
    def wrap(request, id_field,id):
        lp = get_object_or_404(log_plot,pk=id)
        if lp.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_drilling_author(function):
    def wrap(request, id_field,id):
        drill = get_object_or_404(drilling,pk=id)
        if drill.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_casing_author(function):
    def wrap(request, id_field,id):
        case = get_object_or_404(casing,pk=id)
        if case.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_packing_author(function):
    def wrap(request, id_field,id):
        pack = get_object_or_404(packing,pk=id)
        if pack.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
