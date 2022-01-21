from django.core.exceptions import PermissionDenied
from observe.springs.models import XY_Spring,springdischarge_anual,springdischarge_avg_anual,springdischarge_monthly,springdischarge_avg_monthly\
    ,springdischarge_daily
from django.shortcuts import render, redirect, get_object_or_404

def user_is_springdischarge_anual_author(function):
    def wrap(request, id_field,id):
        springdischarge_anual_new = get_object_or_404(springdischarge_anual,pk=id)
        if springdischarge_anual_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_springdischarge_avg_anual_author(function):
    def wrap(request, id_field,id):
        springdischarge_avg_anual_new = get_object_or_404(springdischarge_avg_anual,pk=id)
        if springdischarge_avg_anual_new.created_by == request.user:
            request.temp_daily = springdischarge_avg_anual_new
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_springdischarge_monthly_author(function):
    def wrap(request, id_field,id):
        springdischarge_monthly_new = get_object_or_404(springdischarge_monthly,pk=id)
        if springdischarge_monthly_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_springdischarge_avg_monthly_author(function):
    def wrap(request, id_field,id):
        springdischarge_avg_monthly_new = get_object_or_404(springdischarge_avg_monthly,pk=id)
        if springdischarge_avg_monthly_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_springdischarge_daily_author(function):
    def wrap(request, id_field,id):
        springdischarge_daily_new = get_object_or_404(springdischarge_daily,pk=id)
        if springdischarge_daily_new.created_by == request.user:
            return function(request,id_field, id)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
