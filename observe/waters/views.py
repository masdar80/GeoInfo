from django.shortcuts import render,get_object_or_404,redirect
from observe.models import waterchemistrysurvey_station,watersampling,fieldparameter,eutrophication2,\
heavymetals_rareelement,hydrochemical,toxic_substances,othercommon_parameters,biological
import psycopg2




from observe.waters.forms import waterchemistrysurvey_stationForm,watersamplingForm,fieldparameterForm,eutrophication2Form,\
heavymetals_rareelementForm,hydrochemicalForm,toxic_substancesForm,othercommon_parametersForm,biologicalForm
from django.core.serializers import serialize
from django.http import HttpResponse
from observe.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse


def all_waterchemistrysurvey_station(request):
    xy_stations = waterchemistrysurvey_station.objects.all()
    map_xy_stations = serialize('geojson', xy_stations)

    context = {
        'xy_stations': xy_stations,
        'map_xy_stations': map_xy_stations,

    }
    return render(request, 'observe/stations.html', context)

class waterchemistrysurvey_stationListView( BaseListView):
    model = waterchemistrysurvey_station
    paginate_by = 100  # if pagination is desired

class waterchemistrysurvey_stationCreate( LoginRequiredMixin, BaseCreateView):
    model = waterchemistrysurvey_station
    form_class = waterchemistrysurvey_stationForm

    def form_valid(self, form):
        created_by = self.request.user
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'Your point was  saved successfully!')
        return super().form_valid(form)


class waterchemistrysurvey_stationUpdate( LoginRequiredMixin,BaseUpdateView):
    model = waterchemistrysurvey_station
    form_class = waterchemistrysurvey_stationForm
    template_name = 'observe/water/water_station_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        waterstation = self.get_object()
        if self.request.user == waterstation.created_by:
            return True
        else:
            return False



class waterchemistrysurvey_stationDelete( LoginRequiredMixin,BaseDeleteView):
    model = waterchemistrysurvey_station
    success_url = '/stations'
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


###############

def watersample_list(request,waterchemistrysurvey_station_id):
    xy_station = get_object_or_404(waterchemistrysurvey_station, pk=waterchemistrysurvey_station_id)
    map_xy_station = serialize('geojson', waterchemistrysurvey_station.objects.filter(pk=waterchemistrysurvey_station_id))
    print(map_xy_station)
    print(waterchemistrysurvey_station_id)
    watersamplingsnew = xy_station.watersamplings.all()

    context={
        'watersamplingsnew':watersamplingsnew,
        'waterchemistrysurvey_station_id':waterchemistrysurvey_station_id,
        'map_xy_station':map_xy_station,
    }
    return render(request,'observe/water/watersample_list.html',context)

def watersample_form(request, waterchemistrysurvey_station_id ,sample_id=0):
    water_station = get_object_or_404(waterchemistrysurvey_station, pk=waterchemistrysurvey_station_id)

    if request.method=="GET":
        if sample_id==0:
            form = watersamplingForm()
        else:
            watersamplingnew = watersampling.objects.filter(pk=sample_id).first()
            form = watersamplingForm(instance=watersamplingnew)
        context = {'form': form,'waterchemistrysurvey_station_id':waterchemistrysurvey_station_id}
        return render(request, 'observe/water/watersample_form.html',context)
    else:
        if sample_id==0:
            form = watersamplingForm(request.POST)
            new_form = form.save(commit=False)
            new_form.waterchemistrysurvey_station = water_station
            new_form.save()
        else:
            watersamplingnew = watersampling.objects.filter(pk=sample_id).first()
            form = watersamplingForm(request.POST,instance=watersamplingnew)
        if form.is_valid():
            form.save()
        return redirect('watersample-list', waterchemistrysurvey_station_id)

def watersample_delete(request ,waterchemistrysurvey_station_id,sample_id):
    deleted_watersampling = watersampling.objects.get(pk=sample_id)
    deleted_watersampling.delete()
    return redirect('watersampe-list', waterchemistrysurvey_station_id)

#############
def fieldparameter_list(request,watersampling_id):

    water_sample = get_object_or_404(watersampling, pk=watersampling_id)
    waterstation_id = water_sample.waterchemistrysurvey_station.id_pk
    fieldparameters = water_sample.fieldparameters.all()

    context={
        'fieldparameters':fieldparameters,
        'watersampling_id':watersampling_id,
        'waterstation_id':waterstation_id

    }
    return render(request,'observe/water/fieldparameter_list.html',context)
def fieldparameter_form(request, watersampling_id ,id=0):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)

    if request.method=="GET":
        if id==0:
            form = fieldparameterForm()
        else:
            fieldparameternew = fieldparameter.objects.filter(pk=id).first()
            form = fieldparameterForm(instance=fieldparameternew)
        context = {'form': form,'watersampling_id':watersampling_id}
        return render(request, 'observe/water/fieldparameter_form.html',context)
    else:
        if id==0:
            form = fieldparameterForm(request.POST)
            new_form = form.save(commit=False)
            new_form.watersampling = water_sample
            new_form.save()
        else:
            fieldparameternew = fieldparameter.objects.filter(pk=id).first()
            form = fieldparameterForm(request.POST,instance=fieldparameternew)
        if form.is_valid():
            form.save()
        return redirect('fieldparameter-list', watersampling_id)

def fieldparameter_delete(request ,watersampling_id,id):
    deleted_fieldparameter = fieldparameter.objects.get(pk=id)
    deleted_fieldparameter.delete()
    return redirect('fieldparameter-list', watersampling_id)
######################
def eutrophication2_list(request, watersampling_id):

    water_sample = get_object_or_404(watersampling, pk=watersampling_id)
    waterstation_id = water_sample.waterchemistrysurvey_station.id_pk
    eutrophication2s = water_sample.eutrophication2s.all()

    context = {
        'eutrophication2s': eutrophication2s,
        'watersampling_id': watersampling_id,
        'waterstation_id':waterstation_id
    }
    return render(request, 'observe/water/eutrophication2_list.html', context)
def eutrophication2_form(request, watersampling_id ,id=0):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)

    if request.method=="GET":
        if id==0:
            form = eutrophication2Form()
        else:
            eutrophication2new = eutrophication2.objects.filter(pk=id).first()
            form = eutrophication2Form(instance=eutrophication2new)
        context = {'form': form,'watersampling_id':watersampling_id}
        return render(request, 'observe/water/eutrophication2_form.html',context)
    else:
        if id==0:
            form = eutrophication2Form(request.POST)
            new_form = form.save(commit=False)
            new_form.watersampling = water_sample
            new_form.save()
        else:
            eutrophication2new = eutrophication2.objects.filter(pk=id).first()
            form = eutrophication2Form(request.POST,instance=eutrophication2new)
        if form.is_valid():
            form.save()
        return redirect('eutrophication2-list', watersampling_id)

def eutrophication2_delete(request ,watersampling_id,id):
    deleted_eutrophication2 = eutrophication2.objects.get(pk=id)
    deleted_eutrophication2.delete()
    return redirect('eutrophication2-list', watersampling_id)
#########################

def heavymetals_rareelement_list(request, watersampling_id):

    water_sample = get_object_or_404(watersampling, pk=watersampling_id)
    waterstation_id = water_sample.waterchemistrysurvey_station.id_pk
    heavymetals_rareelements = water_sample.heavymetals_rareelements.all()

    context = {
        'heavymetals_rareelements': heavymetals_rareelements,
        'waterstation_id':waterstation_id,
        'watersampling_id': watersampling_id,
    }
    return render(request, 'observe/water/heavymetals_rareelement_list.html', context)
def heavymetals_rareelement_form(request, watersampling_id ,id=0):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)

    if request.method=="GET":
        if id==0:
            form = heavymetals_rareelementForm()
        else:
            heavymetals_rareelementnew = heavymetals_rareelement.objects.filter(pk=id).first()
            form = heavymetals_rareelementForm(instance=heavymetals_rareelementnew)
        context = {'form': form,'watersampling_id':watersampling_id}
        return render(request, 'observe/water/heavymetals_rareelement_form.html',context)
    else:
        if id==0:
            form = heavymetals_rareelementForm(request.POST)
            new_form = form.save(commit=False)
            new_form.watersampling = water_sample
            new_form.save()
        else:
            heavymetals_rareelementnew = heavymetals_rareelement.objects.filter(pk=id).first()
            form = heavymetals_rareelementForm(request.POST,instance=heavymetals_rareelementnew)
        if form.is_valid():
            form.save()
        return redirect('heavymetals-rareelement-list', watersampling_id)

def heavymetals_rareelement_delete(request ,watersampling_id,id):
    deleted_heavymetals_rareelement = heavymetals_rareelement.objects.get(pk=id)
    deleted_heavymetals_rareelement.delete()
    return redirect('heavymetals-rareelement-list', watersampling_id)
##################
def hydrochemical_list(request,watersampling_id):

    water_sample = get_object_or_404(watersampling, pk=watersampling_id)
    waterstation_id = water_sample.waterchemistrysurvey_station.id_pk
    hydrochemicals = water_sample.hydrochemicals.all()

    context = {
        'hydrochemicals': hydrochemicals,
        'watersampling_id': watersampling_id,
        'waterstation_id':waterstation_id
    }
    return render(request, 'observe/water/hydrochemical_list.html', context)
def hydrochemical_form(request, watersampling_id ,id=0):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)

    if request.method=="GET":
        if id==0:
            form = hydrochemicalForm()
        else:
            hydrochemicalnew = hydrochemical.objects.filter(pk=id).first()
            form = hydrochemicalForm(instance=hydrochemicalnew)
        context = {'form': form,'watersampling_id':watersampling_id}
        return render(request, 'observe/water/hydrochemical_form.html',context)
    else:
        if id == 0:
            form = hydrochemicalForm(request.POST)
            new_form = form.save(commit=False)
            new_form.watersampling = water_sample
            new_form.save()
        else:
            hydrochemicalnew1 = hydrochemical.objects.filter(pk=id).first()
            form = hydrochemicalForm(request.POST, instance=hydrochemicalnew1)
            if form.is_valid():
             form.save()
        return redirect('hydrochemical-list', watersampling_id)
def hydrochemical_delete(request ,watersampling_id,id):
    deleted_hydrochemical = hydrochemical.objects.get(pk=id)
    deleted_hydrochemical.delete()
    return redirect('hydrochemical-list', watersampling_id)
###############
def toxic_substances_list(request, watersampling_id):

    water_sample = get_object_or_404(watersampling, pk=watersampling_id)
    waterstation_id = water_sample.waterchemistrysurvey_station.id_pk
    toxic_substancess = water_sample.toxic_substancess.all()

    context = {
        'toxic_substancess': toxic_substancess,
        'waterstation_id': waterstation_id,
        'watersampling_id': watersampling_id,
    }
    return render(request, 'observe/water/toxic_substances_list.html', context)
def toxic_substances_form(request, watersampling_id ,id=0):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)

    if request.method=="GET":
        if id==0:
            form = toxic_substancesForm()
        else:
            toxic_substancesnew = toxic_substances.objects.filter(pk=id).first()
            form = toxic_substancesForm(instance=toxic_substancesnew)
        context = {'form': form,'watersampling_id':watersampling_id}
        return render(request, 'observe/water/toxic_substances_form.html',context)
    else:
        if id == 0:
            form = toxic_substancesForm(request.POST)
            new_form = form.save(commit=False)
            new_form.watersampling = water_sample
            new_form.save()
        else:
            toxic_substancesnew1 = toxic_substances.objects.filter(pk=id).first()
            form = toxic_substancesForm(request.POST, instance=toxic_substancesnew1)
            if form.is_valid():
             form.save()
        return redirect('toxic-substances-list', watersampling_id)
def toxic_substances_delete(request ,watersampling_id,id):
    deleted_toxic_substances = toxic_substances.objects.get(pk=id)
    deleted_toxic_substances.delete()
    return redirect('toxic-substances-list', watersampling_id)
############
def othercommon_parameters_list(request,  watersampling_id):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)
    waterstation_id = water_sample.waterchemistrysurvey_station.id_pk

    othercommon_parameterss = water_sample.othercommon_parameterss.all

    context = {
        'othercommon_parameterss': othercommon_parameterss,
        'waterstation_id': waterstation_id,
        'watersampling_id': watersampling_id,
    }
    return render(request, 'observe/water/othecommon_parameters_list.html', context)
def othercommon_parameters_form(request, watersampling_id ,id=0):
    water_sample = get_object_or_404(watersampling, pk=watersampling_id)

    if request.method=="GET":
        if id==0:
            form = othercommon_parametersForm()
        else:
            othercommon_parameters0 = othercommon_parameters.objects.filter(pk=id).first()
            form = othercommon_parametersForm(instance=othercommon_parameters0)
        context = {'form': form,'watersampling_id':watersampling_id}
        return render(request, 'observe/water/othercommon_parameters_form.html',context)
    else:
        if id == 0:
            form = othercommon_parametersForm(request.POST)
            new_form = form.save(commit=False)
            new_form.watersampling = water_sample
            new_form.save()
        else:
            othercommon_parameters1 = othercommon_parameters.objects.filter(pk=id).first()
            form = othercommon_parametersForm(request.POST, instance=othercommon_parameters1)
            if form.is_valid():
             form.save()
        return redirect('othercommon-parameters-list', watersampling_id)
def othercommon_parameters_delete(request ,watersampling_id,id):
    deleted_othercommon_parameters = othercommon_parameters.objects.get(pk=id)
    deleted_othercommon_parameters.delete()
    return redirect('othercommon-parameters-list', watersampling_id)
###########
def biological_list(request, xy_station_id, sample_id):
    xy_station = get_object_or_404(waterchemistrysurvey_station, pk=xy_station_id)
    map_xy_stations = serialize('geojson', waterchemistrysurvey_station.objects.filter(pk=xy_station_id))
    ##############groundwaterlevels#############
    water_sample = get_object_or_404(watersampling, pk=sample_id)

    fieldparameters = water_sample.fieldparameters

    context = {
        'fieldparameters': fieldparameters,
        'xy_station_id': xy_station_id,
        'sample_id': sample_id,
    }
    return render(request, 'observe/sample/details_list.html', context)