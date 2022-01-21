from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.gis.geos import Point

import csv
import xlwt
import json
from observe.utils.filter import filter_date
from observe.metologys.models import Metology_inf, XY_Metology, airpressure, evaporation_daily, evaporation_monthly, \
    precipitation_daily, \
    humidity_monthly, humidity_daily, temperature_daily, temperature_monthly, precipitation_monthly, \
    precipitation_annual, \
    wind_daily, wind_monthly, sunshine_daily, Metology_inf
from observe.metologys.filter import filter_evaporation_daily, filter_evaporation_monthly, filter_airpressure, \
    filter_humidity_daily, filter_precipitation_annual, \
    filter_humidity_monthly, filter_precipitation_daily, filter_precipitation_monthly, filter_sunshine_daily, \
    filter_temperature_daily, filter_temperature_monthly, \
    filter_wind_daily, filter_wind_monthly,filter_snowdepth,filter_snowfall
from observe.metologys.forms import humedity_dailyForm, QueryForm, QueryDateForm, humedity_monthlyForm, airpressureForm, \
    temperature_dailyForm, temperature_monthlyForm, evaporation_dailyForm, evaporation_monthlyForm, \
    precipitation_dailyForm, precipitation_monthlyForm, precipitation_annualForm, wind_dailyForm, wind_monthlyForm, \
    sunshine_dailyForm, metology_infForm,snowdepthForm,snowfallForm,QueryAnuallDateForm

from .resources import evaporation_dailyResource, airpressureResource, evaporation_monthlyResource, \
    humidity_dailyResource, humidity_monthlyResource,snowdepthResource,snowfallResource ,\
    temperature_dailyResource, temperature_monthlyResource, precipitation_annualResource, precipitation_dailyResource, \
    precipitation_monthlyResource, \
    wind_dailyResource, wind_monthlyResource, sunshine_dailyResource
from observe.metologys.decorators import user_is_air_pressure_author, user_is_ed_author, user_is_em_author, \
    user_is_hd_author, user_is_hm_author, user_is_pa_author, \
    user_is_pd_author, user_is_pm_author, user_is_sd_author, user_is_td_author, \
    user_is_temp_daily_author, user_is_temp_monthly_author, user_is_tm_author, user_is_wd_author ,\
    user_is_wm_author,user_is_snowfall_author,user_is_snowdepth_author

from observe.utils.filter import filter_waterpoints
from tablib import Dataset
from observe.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from observe.metologys.forms import MetologyForm
from django.contrib import messages
from django.utils import timezone
from observe.metologys.models import *
from observe.utils.utils import render_to_pdf

import statistics
import scipy.stats


################# add edit delete metology point

class MetologyListView(BaseListView):
    model = XY_Metology
    paginate_by = 100  # if pagination is desired


class MetologyCreate(LoginRequiredMixin, BaseCreateView):
    model = XY_Metology
    form_class = MetologyForm
    def form_valid(self, form):
        image = self.request.FILES.get('image')
        created_by = self.request.user
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'Your point was  saved successfully!')
        return super().form_valid(form)



class MetologyUpdate(LoginRequiredMixin, BaseUpdateView):
    model = XY_Metology
    form_class = MetologyForm
    template_name = 'observe/metology_form.html'

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        xy_metology = self.get_object()
        if self.request.user == xy_metology.created_by:
            return True
        else:
            return False


class MetologyDelete(LoginRequiredMixin, UserPassesTestMixin, BaseDeleteView):
    model = XY_Metology
    success_url = '/xy_metologys'

    def test_func(self):
        xy_metology = self.get_object()
        if self.request.user == xy_metology.created_by:
            return True
        else:
            return False


##############import evaporation_daily

def simple_upload(request, id_field):
    if request.method == 'POST':
        evaporation_daily_resource = evaporation_dailyResource()
        dataset = Dataset()
        new_evaporation_dailys = request.FILES['myfile']

        imported_data = dataset.load(new_evaporation_dailys.read())
        result = evaporation_daily_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            evaporation_daily_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'observe/metology/metology_ed_list.html', {'id_field': id_field})


############
def import_metology_readings(request):
    XY_Metologys = XY_Metology.objects.all()

    map_XY_Metologys = serialize('geojson', XY_Metologys)


    context = {
        'XY_Metologys': XY_Metologys,
        'map_XY_Metologys': map_XY_Metologys,

    }
    return render(request,'observe/metology_import_form.html',context)

######################

@login_required
def all_xy_metologys(request):
    XY_Metologys = XY_Metology.objects.all()
    form = QueryForm(request.GET or None)
    paramDict = request.GET
    XY_Metologys = filter_waterpoints(XY_Metologys, paramDict)
    map_XY_Metologys = serialize('geojson', XY_Metologys)
    print(map_XY_Metologys)

    context = {
        'XY_Metologys': XY_Metologys,
        'map_XY_Metologys': map_XY_Metologys,
        'form': form,
    }
    return render(request, 'observe/metologys.html', context)


######################start airpresure #########

def air_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    xy_metology_information = xy_metology.metology_inf

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=xy_metology.pk))
    id_field = xy_metology.id_field
    airpressures = xy_metology.airpressures.filter(created_by=request.user)

    paramDict = request.GET
    airpressures_new = filter_airpressure(airpressures, paramDict)

    x = list()
    for entry in airpressures_new:
        x.append(entry.daily_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)

    max_x = max(x)
    min_x = min(x)
    count_x = len(x)

    today = timezone.now()

    params = {
        'today': today,
        'airpressures_new': airpressures_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'xy_metology': xy_metology,
        'max_x': max_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,
        'count_x': count_x

    }
    pdf = render_to_pdf('observe/metology/air_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


def air_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    xy_metology_information = xy_metology.metology_inf
    print(xy_metology_information)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=xy_metology.pk))
    id_field = xy_metology.id_field
    airpressures = xy_metology.airpressures.filter(created_by=request.user)

    paramDict = request.GET
    airpressures_new = filter_airpressure(airpressures, paramDict)

    for entry in airpressures_new:
        y = list()
        for entry in airpressures_new:
            y.append(entry.daily_max)
        mean_y = statistics.mean(y)
        median_y = statistics.median(y)
        mode_y = statistics.multimode(y)
        max_y = max(y)
        min_y = min(y)
        count_y = len(y)
        today = timezone.now()

    params = {
        'today': today,
        'airpressures_new': airpressures_new,
        'xy_metology_information': xy_metology_information,
        'mean_y': mean_y,
        'xy_metology': xy_metology,
        'max_y': max_y,
        'min_y': min_y,
        'count_y': count_y,
        'median_y': median_y,
        'mode_y': mode_y,
        'mean_y': mean_y,

    }
    pdf = render_to_pdf('observe/metology/air_max_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


def air_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=xy_metology.pk))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    airpressures = xy_metology.airpressures.filter(created_by=request.user)

    paramDict = request.GET
    airpressures_new = filter_airpressure(airpressures, paramDict)

    z = list()
    for entry in airpressures_new:
        z.append(entry.daily_min)
        mean_z = statistics.mean(z)
        median_z = statistics.median(z)
        mode_z = statistics.multimode(z)
        max_z = max(z)
        min_z = min(z)
        count_z = len(z)
        today = timezone.now()
    params = {
        'today': today,
        'airpressures_new': airpressures_new,
        'xy_metology_information': xy_metology_information,
        'mean_z': mean_z,
        'xy_metology': xy_metology,
        'max_z': max_z,
        'min_z': min_z,
        'count_z': count_z,
        'median_z': median_z,
        'mode_z': mode_z,
        'mean_z': mean_z

    }
    pdf = render_to_pdf('observe/metology/air_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


def create_pdf_report(request, id_field):
    pdf = SimpleDocTemplate("myfile.pdf", pagesize=letter)
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    xy_metology_information = xy_metology.metology_inf
    airpressures = xy_metology.airpressures.all()

    paramDict = request.GET
    airpressures_new = filter_airpressure(airpressures, paramDict)

    def genPointTable():
        PointElemTable = None

        pointElemWidth = 500
        # 1) Build Structure
        titleTable = Table([
            ["report about id_field:", xy_metology.id_field]
        ], 250, 250)
        info_pointTable = Table([
            "village:", xy_metology.village, "mohafaza:", xy_metology.village, "montika:", xy_metology.montika,
            "nahia:", xy_metology.nahia]
            , 62, 63, 62, 63, 62, 63, 62, 63)
        names_table = Table([
            "arabic_name:", xy_metology.sitename_a, "english_name:", xy_metology.sitename_e], 60, 60, 60, 60)
        point_coordinate_table = Table(["point_coordinate:", xy_metology.geom], 100)
        name_coordinate_table = Table([names_table, point_coordinate_table], 240)
        pic_table = Table(["image:", xy_metology.image.url], 100, 100)
        pic_name_coordiante_table = Table([name_coordinate_table, pic_table], 250, 250)
        PointElemTable = Table([titleTable, info_pointTable, pic_name_coordiante_table], pointElemWidth)
        return PointElemTable

    # def statisticsTable():
    #     statisticTable = None
    #
    #     titleTable = Table([
    #         ["statistics results:", airpressures_new.max(),airpressures_new.min()]
    #     ], 60)
    #     statisticTable = Table([titleTable],240)
    #     return statisticTable
    #
    # def getLineChart():
    #
    #
    #     today = timezone.now()
    #     categories = list()
    #     daily_avg_series_data = list()
    #
    #     for entry in airpressures_new:
    #         categories.append(entry.obs_datetime)
    #         daily_avg_series_data.append(entry.daily_avg)
    #
    #     data = daily_avg_series_data
    #
    #     chart = HorizontalLineChart()
    #     chart.data = data
    #     chart.x = 5
    #     chart.y = 5
    #     chart.height = 100
    #     chart.width = 240
    #
    #     chart.categoryAxis.categoryNames = categories
    #
    #     title = String(
    #         50, 110,
    #         'Line Chart',
    #         fontSize=14
    #     )
    #
    #     chart.valueAxis.valueMin = 0
    #     chart.valueAxis.valueMax = 10
    #     chart.valueAxis.valueStep = 2
    #
    #     chart.lines[0].strokeWidth = 3.5
    #     chart.lines[1].strokeWidth = 1
    #     chart.lines[0].strokeColor = colors.pink
    #
    #     drawing = Drawing(240, 120)
    #     drawing.add(title)
    #     drawing.add(chart)
    #
    #     return drawing

    table = Table([
        [genPointTable]
        # [getLineChart],
        # [statisticsTable]
    ], 500)

    # table.setStyle([
    #     ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
    #     # ("VALIGN", (0, 0), (-1, -1), "CENTER"),
    #     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    # ])

    elems = []
    elems.append(table)
    pdf.build(elems)
    return HttpResponse(pdf, content_type='application/pdf')


def report_xy_metologys(request):
    XY_Metologys = XY_Metology.objects.all()
    map_XY_Metologys = serialize('geojson', XY_Metologys)
    form = QueryForm(request.GET or None)
    id_fields = []
    air_pressurs = []
    paramDict = request.GET
    XY_Metologys = filter_waterpoints(XY_Metologys, paramDict)
    print(XY_Metologys.count())
    map_XY_Metologys = serialize('geojson', XY_Metologys)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    for xy in XY_Metologys:
        xy_metology = get_object_or_404(XY_Metology, pk=xy.pk)
        id_fields.append(xy.id_field)

    for i in range(len(id_fields)):
        airpressures_new = []
        xy_metology = XY_Metology.objects.get(id_field=id_fields[i])
        airpressuress = xy_metology.airpressures.all()
        airpressures_new.append(filter_airpressure(airpressuress, paramDict))

    print(id_fields)
    print(airpressures_new)
    context = {
        'form_date': form_date,
        'XY_Metologys': XY_Metologys,
        'map_XY_Metologys': map_XY_Metologys,
        'form': form,
        'id_fields': id_fields,
        'air_pressurs': air_pressurs,

    }
    return render(request, 'observe/metology/report-air.html', context)


@login_required
def metology_air_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    airpressures = xy_metology.airpressures.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    airpressures_new = filter_airpressure(airpressures, paramDict)

    context = {
        'metologyinfnew': metologyinfnew,
        'airpressures_new': airpressures_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology
    }
    return render(request, 'observe/metology/metology_air_list.html', context)


@login_required
def metology_air_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = airpressureForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('air-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('air-list', id_field)

    elif (request.method == "GET"):
        form = airpressureForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/air_form.html', context)


@login_required
@user_is_air_pressure_author
def metology_air_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        airpressurenew = airpressure.objects.filter(pk=id).first()
        form = airpressureForm(instance=airpressurenew)

        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/air_form.html', context)
    elif request.method == "POST":

        airpressurenew = airpressure.objects.filter(pk=id).first()
        form = airpressureForm(request.POST, instance=airpressurenew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('air-list', id_field)
        else:
            messages.warning(request, 'the updated failed!')
            return redirect('air-list', id_field)


@login_required
@user_is_air_pressure_author
def metology_air_delete(request, id_field, id):
    deleted_airpressure = airpressure.objects.get(pk=id)
    deleted_airpressure.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('air-list', id_field)
@login_required
@user_is_air_pressure_author
def metology_air_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    airpressures = xy_metology.airpressures.filter(waterpoint_id=id_field)
    airpressures = filter_airpressure(airpressures, paramDict)

    paramDict = request.GET
    airpressures = filter_airpressure(airpressures, paramDict)
    for airpressure in airpressures:
        airpressure.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('air-list', id_field)



@login_required
def export_airpressur(request, id_field):
    airpressure_resource = airpressureResource()
    paramDict = request.GET
    airpressures = airpressure.objects.filter(waterpoint_id=id_field)
    airpressures = filter_airpressure(airpressures, paramDict)

    dataset = airpressure_resource.export(airpressures)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="airpressur.xls"'
    return response


################ Metology_inf
def metology_inf_update_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)

    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()
    if request.method == "GET":
        form = metology_infForm(instance=metologyinfnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/metologyinf_form.html', context)
    elif request.method == "POST":

        form = metology_infForm(request.POST, instance=metologyinfnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('xy_metologys')


######################start evaporation_daily #########

@login_required
def ed_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=xy_metology.pk))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    evaporation_dailys = xy_metology.evaporation_dailys.filter(created_by=request.user)

    paramDict = request.GET
    evaporation_daily_new = filter_evaporation_daily(evaporation_dailys, paramDict)

    x = list()
    for entry in evaporation_daily_new:
        x.append(entry.evap_mm)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'evaporation_daily_new': evaporation_daily_new,
        'xy_metology_information': xy_metology_information,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,
        'count_x': count_x

    }
    pdf = render_to_pdf('observe/metology/ed_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def metology_ed_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.get(xy_metology=xy_metology.pk)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    evaporation_dailys = xy_metology.evaporation_dailys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    evaporation_dailys_new = filter_evaporation_daily(evaporation_dailys, paramDict)

    context = {
        'metologyinfnew': metologyinfnew,
        'evaporation_dailys_new': evaporation_dailys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,

    }
    return render(request, 'observe/metology/metology_ed_list.html', context)


@login_required
def metology_ed_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = evaporation_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added  successfully!')
            return redirect('ed-list', id_field)
        else:
            messages.warning(request, 'sorry the added  failed!')
            return redirect('ed-list', id_field)

    elif (request.method == "GET"):
        form = evaporation_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/ed_form.html', context)


@login_required
@user_is_ed_author
def metology_ed_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        evaporation_dailynew = evaporation_daily.objects.filter(pk=id).first()
        form = evaporation_dailyForm(instance=evaporation_dailynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/ed_form.html', context)
    elif request.method == "POST":

        evaporation_dailynew = evaporation_daily.objects.filter(pk=id).first()
        form = evaporation_dailyForm(request.POST, instance=evaporation_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done  successfully!')
            return redirect('ed-list', id_field)
        else:
            messages.warning(request, 'the updated failed!')
            return redirect('ed-list', id_field)


@login_required
@user_is_ed_author
def metology_ed_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    evaporation_dailys = xy_metology.evaporation_dailys.filter(waterpoint_id=id_field)
    evaporation_dailys = filter_evaporation_daily(evaporation_dailys, paramDict)

    paramDict = request.GET
    airpressures = filter_evaporation_daily(evaporation_dailys, paramDict)
    for airpressure in airpressures:
        airpressure.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('ed-list', id_field)


@login_required
@user_is_ed_author
def metology_ed_delete(request, id_field, id):
    deleted_evaporation_daily = evaporation_daily.objects.get(pk=id)
    deleted_evaporation_daily.delete()
    messages.success(request, 'the deleted done  successfully!')
    return redirect('ed-list', id_field)


@login_required
def export_evaporation_daily(request, id_field):
    evaporation_daily_resource = evaporation_dailyResource()
    paramDict = request.GET
    evaporation_dailys = evaporation_daily.objects.filter(waterpoint_id=id_field)
    evaporation_dailys_ = filter_evaporation_daily(evaporation_dailys, paramDict)

    dataset = evaporation_daily_resource.export(evaporation_dailys_)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="evaporation_daily.xls"'
    return response


#####################start evaporation_monthly #########
@login_required
def metology_em_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    evaporation_monthlys = xy_metology.evaporation_monthlys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    evaporation_monthlys_new = filter_evaporation_monthly(evaporation_monthlys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'evaporation_monthlys_new': evaporation_monthlys_new,
        'id_field': id_field,
        'xy_metology': xy_metology,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,
    }
    return render(request, 'observe/metology/metology_em_list.html', context)


@login_required
def metology_em_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = evaporation_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('em-list', id_field)
        else:
            messages.warning(request, 'sorry the  added failed!')
            return redirect('em-list', id_field)

    elif (request.method == "GET"):
        form = evaporation_monthlyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/em_form.html', context)


@login_required
@user_is_em_author
def metology_em_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        evaporation_monthlynew = evaporation_monthly.objects.filter(pk=id).first()
        form = evaporation_monthlyForm(instance=evaporation_monthlynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/em_form.html', context)
    elif request.method == "POST":

        evaporation_monthlynew = evaporation_monthly.objects.filter(pk=id).first()
        form = evaporation_monthlyForm(request.POST, instance=evaporation_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('em-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('em-list', id_field)


@login_required
@user_is_em_author
def metology_em_delete(request, id_field, id):
    deleted_evaporation_monthly = evaporation_monthly.objects.get(pk=id)
    deleted_evaporation_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('em-list', id_field)

@login_required
@user_is_em_author
def metology_em_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    evaporation_monthlys = xy_metology.evaporation_monthlys.filter(waterpoint_id=id_field)
    evaporation_monthlys = filter_evaporation_monthly(evaporation_monthlys, paramDict)

    paramDict = request.GET
    evaporation_monthlys = filter_evaporation_monthly(evaporation_monthlys, paramDict)
    for evaporation_monthly in evaporation_monthlys:
        evaporation_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('em-list', id_field)

@login_required
def em_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    evaporation_monthlys = xy_metology.evaporation_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    evaporation_monthlys_new = filter_evaporation_monthly(evaporation_monthlys, paramDict)

    x = list()
    for entry in evaporation_monthlys_new:
        x.append(entry.monthly_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'evaporation_monthlys_new': evaporation_monthlys_new,
        'xy_metology_information': xy_metology_information,
        'count_x': count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/em_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def export_evaporation_monthly(request, id_field):
    evaporation_monthly_resource = evaporation_monthlyResource()
    paramDict = request.GET
    evaporation_monthlys = evaporation_monthly.objects.filter(waterpoint_id=id_field)
    evaporation_monthlys = filter_evaporation_monthly(evaporation_monthlys, paramDict)

    dataset = evaporation_monthly_resource.export(evaporation_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="evaporation_monthly.xls"'
    return response


#####################start humidity_daily #########
@login_required
def metology_hd_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    humidity_dailys = xy_metology.humidity_dailys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    humidity_dailys_new = filter_humidity_daily(humidity_dailys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'humidity_dailys_new': humidity_dailys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,
    }
    return render(request, 'observe/metology/metology_hd_list.html', context)


@login_required
def metology_hd_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = humedity_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('hd-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('hd-list', id_field)

    elif (request.method == "GET"):
        form = humedity_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/hd_form.html', context)


@login_required
@user_is_hd_author
def metology_hd_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        humidity_dailynew = humidity_daily.objects.filter(pk=id).first()
        form = humedity_dailyForm(instance=humidity_dailynew)

        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/hd_form.html', context)
    elif request.method == "POST":

        humidity_dailynew = humidity_daily.objects.filter(pk=id).first()
        form = humedity_dailyForm(request.POST, instance=humidity_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('hd-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('hd-list', id_field)


@login_required
@user_is_hd_author
def metology_hd_delete(request, id_field, id):
    deleted_humedity_daily = humedity_dailyForm.objects.get(pk=id)
    deleted_humedity_daily.delete()
    messages.success(request, 'the deleted done successfully')

    return redirect('hd-list', id_field)

@login_required
@user_is_hd_author
def metology_hd_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    humidity_dailys = xy_metology.humidity_dailys.filter(waterpoint_id=id_field)
    humidity_dailys = filter_humidity_daily(humidity_dailys, paramDict)

    paramDict = request.GET
    humidity_dailys = filter_humidity_daily(humidity_dailys, paramDict)
    for humidity_daily in humidity_dailys:
        humidity_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('hd-list', id_field)

@login_required
def export_humidity_daily(request, id_field):
    humidity_daily_resource = humidity_dailyResource()
    paramDict = request.GET
    humidity_dailys = humidity_daily.objects.filter(waterpoint_id=id_field)
    humidity_dailys = filter_humidity_daily(humidity_dailys, paramDict)

    dataset = humidity_daily_resource.export(humidity_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="humidity_daily.xls"'
    return response

@login_required
def hd_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    humidity_dailys = xy_metology.humidity_dailys.filter(created_by=request.user)

    paramDict = request.GET
    humidity_dailys_new = filter_humidity_daily(humidity_dailys, paramDict)

    x = list()
    for entry in humidity_dailys_new:
        x.append(entry.daily_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'humidity_dailys_new': humidity_dailys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'count_x': count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/hd_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def hd_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    humidity_dailys = xy_metology.humidity_dailys.filter(created_by=request.user)

    paramDict = request.GET
    humidity_dailys_new = filter_humidity_daily(humidity_dailys, paramDict)

    x = list()
    for entry in humidity_dailys_new:
        x.append(entry.daily_max)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'humidity_dailys_new': humidity_dailys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'count_x': count_x,

        'xy_metology': xy_metology,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/hd_max_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def hd_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    humidity_dailys = xy_metology.humidity_dailys.filter(created_by=request.user)

    paramDict = request.GET
    humidity_dailys_new = filter_humidity_daily(humidity_dailys, paramDict)

    x = list()
    for entry in humidity_dailys_new:
        x.append(entry.daily_min)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'humidity_dailys_new': humidity_dailys_new,
        'xy_metology_information': xy_metology_information,
        'count_x': count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/hd_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start humidity_monthly #########
@login_required
def metology_hm_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    print(map_xy_metology)

    humidity_monthlys = xy_metology.humidity_monthlys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    humidity_monthlys_new = filter_humidity_monthly(humidity_monthlys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'humidity_monthlys_new': humidity_monthlys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,
    }
    return render(request, 'observe/metology/metology_hm_list.html', context)


@login_required
def metology_hm_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = humedity_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('hm-list', id_field)
        else:
            messages.warning(request, 'sorry the  added failed!')
            return redirect('hm-list', id_field)

    elif (request.method == "GET"):
        form = humedity_monthlyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/hm_form.html', context)


@login_required
@user_is_hm_author
def metology_hm_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        humidity_monthlynew = humidity_monthly.objects.filter(pk=id).first()
        form = humedity_monthlyForm(instance=humidity_monthlynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/hm_form.html', context)
    elif request.method == "POST":

        humidity_monthlynew = humidity_monthly.objects.filter(pk=id).first()
        form = humedity_monthlyForm(request.POST, instance=humidity_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('hm-list', id_field)
        else:
            messages.warning(request, 'sorry the updatedfailed!')
            return redirect('hm-list', id_field)


@login_required
@user_is_hm_author
def metology_hm_delete(request, id_field, id):
    deleted_humidity_monthly = humidity_monthly.objects.get(pk=id)
    deleted_humidity_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('hm-list', id_field)

@login_required
@user_is_hm_author
def metology_hm_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    humidity_monthlys = xy_metology.humidity_monthlys.filter(waterpoint_id=id_field)
    humidity_monthlys = filter_humidity_monthly(humidity_monthlys, paramDict)

    paramDict = request.GET
    humidity_monthlys = filter_humidity_monthly(humidity_monthlys, paramDict)
    for humidity_monthly in humidity_monthlys:
        humidity_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('hm-list', id_field)

@login_required
def export_humidity_monthly(request, id_field):
    humidity_monthly_resource = humidity_monthlyResource()
    paramDict = request.GET
    humidity_monthlys = humidity_monthly.objects.filter(waterpoint_id=id_field)
    humidity_monthlys = filter_humidity_monthly(humidity_monthlys, paramDict)

    dataset = humidity_monthly_resource.export(humidity_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="humidity_monthly.xls"'
    return response

@login_required
def hm_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    humidity_monthlys = xy_metology.humidity_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    humidity_monthlys_new = filter_airpressure(humidity_monthlys, paramDict)

    x = list()
    for entry in humidity_monthlys_new:
        x.append(entry.monthly_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'humidity_monthlys_new': humidity_monthlys_new,
        'xy_metology_information': xy_metology_information,
        'count_x': count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/hm_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def hm_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    humidity_monthlys = xy_metology.humidity_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    humidity_monthlys_new = filter_airpressure(humidity_monthlys, paramDict)

    x = list()
    for entry in humidity_monthlys_new:
        x.append(entry.monthly_max)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'humidity_monthlys_new': humidity_monthlys_new,
        'mean_x': mean_x,
        'count_x': count_x,
        'xy_metology_information': xy_metology_information,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/hm_max_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def hm_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    humidity_monthlys = xy_metology.humidity_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    humidity_monthlys_new = filter_airpressure(humidity_monthlys, paramDict)

    x = list()
    for entry in humidity_monthlys_new:
        x.append(entry.monthly_min)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'humidity_monthlys_new': humidity_monthlys_new,
        'mean_x': mean_x,
        'xy_metology_information': xy_metology_information,
        'count_x': count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/hm_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start tempreture_daily #########

login_required
def metology_td_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    temperature_dailys = xy_metology.temperature_dailys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    temperature_dailys_new = filter_temperature_daily(temperature_dailys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'temperature_dailys_new': temperature_dailys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,
    }
    return render(request, 'observe/metology/metology_td_list.html', context)


login_required
def metology_td_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = temperature_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added  successfully!')
            return redirect('td-list', id_field)
        else:
            messages.warning(request, 'sorry the  added  failed!')
            return redirect('td-list', id_field)

    elif (request.method == "GET"):
        form = temperature_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/td_form.html', context)


@login_required
@user_is_td_author
def metology_td_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        temperature_dailynew = temperature_daily.objects.filter(pk=id).first()
        form = temperature_dailyForm(instance=temperature_dailynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/td_form.html', context)
    elif request.method == "POST":

        temperature_dailynew = temperature_daily.objects.filter(pk=id).first()
        form = temperature_dailyForm(request.POST, instance=temperature_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('td-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed !')
            return redirect('td-list', id_field)


@login_required
@user_is_td_author
def metology_td_delete(request, id_field, id):
    deleted_temperature_daily = temperature_daily.objects.get(pk=id)
    deleted_temperature_daily.delete()
    messages.success(request, 'the deleted done successfully')

    return redirect('td-list', id_field)
@login_required
@user_is_td_author
def metology_td_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    temperature_dailys = xy_metology.temperature_dailys.filter(waterpoint_id=id_field)
    temperature_dailys = filter_temperature_daily(temperature_dailys, paramDict)

    paramDict = request.GET
    temperature_dailys = filter_temperature_daily(temperature_dailys, paramDict)
    for temperature_daily in temperature_dailys:
        humidity_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('td-list', id_field)


@login_required
def export_temperature_daily(request, id_field):
    temperature_daily_resource = temperature_dailyResource()
    paramDict = request.GET
    temperature_dailys = temperature_daily.objects.filter(waterpoint_id=id_field)
    temperature_dailys = filter_humidity_monthly(temperature_dailys, paramDict)

    dataset = temperature_daily_resource.export(temperature_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="temperature_daily.xls"'
    return response

@login_required
def td_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    temperature_dailys = xy_metology.temperature_dailys.filter(created_by=request.user)

    paramDict = request.GET
    temperature_dailys_new = filter_temperature_daily(temperature_dailys, paramDict)

    x = list()
    for entry in temperature_dailys_new:
        x.append(entry.daily_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'temperature_dailys_new': temperature_dailys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'count_x': count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/td_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def td_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    temperature_dailys = xy_metology.temperature_dailys.filter(created_by=request.user)

    paramDict = request.GET
    temperature_dailys_new = filter_temperature_daily(temperature_dailys, paramDict)

    x = list()
    for entry in temperature_dailys_new:
        x.append(entry.daily_max)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'temperature_dailys_new': temperature_dailys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'count_x': count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/td_max_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def td_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    temperature_dailys = xy_metology.temperature_dailys.filter(created_by=request.user)

    paramDict = request.GET
    temperature_dailys_new = filter_temperature_daily(temperature_dailys, paramDict)

    x = list()
    for entry in temperature_dailys_new:
        x.append(entry.daily_min)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'temperature_dailys_new': temperature_dailys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'count_x': count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/td_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start tempreture_monthly #########
@login_required
def metology_tm_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()
    xy_metology_information = xy_metology.metology_inf

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    temperature_monthlys = xy_metology.temperature_monthlys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    temperature_monthlys_new = filter_temperature_monthly(temperature_monthlys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'temperature_monthlys_new': temperature_monthlys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'xy_metology': xy_metology,
        'form_date': form_date
    }
    return render(request, 'observe/metology/metology_tm_list.html', context)


@login_required
def metology_tm_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = temperature_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading  added successfully')
            return redirect('tm-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('tm-list', id_field)


    elif (request.method == "GET"):
        form = temperature_monthlyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/tm_form.html', context)


@login_required
@user_is_tm_author
def metology_tm_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        temperature_monthlynew = temperature_monthly.objects.filter(pk=id).first()
        form = temperature_monthlyForm(instance=temperature_monthlynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/tm_form.html', context)
    elif request.method == "POST":

        temperature_monthlynew = temperature_monthly.objects.filter(pk=id).first()
        form = temperature_monthlyForm(request.POST, instance=temperature_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('tm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed !')
            return redirect('tm-list', id_field)


@login_required
@user_is_tm_author
def metology_tm_delete(request, id_field, id):
    deleted_temperature_monthly = temperature_monthly.objects.get(pk=id)
    temperature_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('tm-list', id_field)

@login_required
@user_is_tm_author
def metology_tm_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    temperature_monthlys = xy_metology.temperature_monthlys.filter(waterpoint_id=id_field)
    temperature_monthlys = filter_temperature_monthly(temperature_monthlys, paramDict)

    paramDict = request.GET
    temperature_monthlys = filter_temperature_monthly(temperature_monthlys, paramDict)
    for temperature_monthly in temperature_monthlys:
        temperature_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('tm-list', id_field)


@login_required
def export_temperature_monthly(request, id_field):
    temperature_monthly_resource = temperature_monthlyResource()
    paramDict = request.GET
    temperature_monthlys = temperature_monthly.objects.filter(waterpoint_id=id_field)
    temperature_monthlys = filter_temperature_monthly(temperature_monthlys, paramDict)

    dataset = temperature_monthly_resource.export(temperature_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="temperature_monthly.xls"'
    return response

@login_required
def tm_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    temperature_monthlys = xy_metology.temperature_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    temperature_monthlys_new = filter_temperature_monthly(temperature_monthlys, paramDict)

    x = list()
    for entry in temperature_monthlys_new:
        x.append(entry.monthly_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'temperature_monthlys_new': temperature_monthlys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'count_x': count_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/tm_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def tm_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    temperature_monthlys = xy_metology.temperature_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    temperature_monthlys_new = filter_temperature_monthly(temperature_monthlys, paramDict)

    x = list()
    for entry in temperature_monthlys_new:
        x.append(entry.monthly_max)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'temperature_monthlys_new': temperature_monthlys_new,
        'mean_x': mean_x,
        'count_x': count_x,
        'xy_metology_information': xy_metology_information,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/tm_max_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def tm_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    temperature_monthlys = xy_metology.temperature_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    temperature_monthlys_new = filter_temperature_monthly(temperature_monthlys, paramDict)

    x = list()
    for entry in temperature_monthlys_new:
        x.append(entry.monthly_min)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'temperature_monthlys_new': temperature_monthlys_new,
        'xy_metology_information': xy_metology_information,
        'count_x': count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/tm_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start precipitation_daily #########
@login_required
def metology_pd_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    precipitation_dailys = xy_metology.precipitation_dailys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    precipitation_dailys_new = filter_precipitation_daily(precipitation_dailys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'precipitation_dailys_new': precipitation_dailys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,
    }
    return render(request, 'observe/metology/metology_pd_list.html', context)


@login_required
def metology_pd_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = precipitation_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('pd-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('pd-list', id_field)

    elif (request.method == "GET"):
        form = precipitation_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/pd_form.html', context)


@login_required
@user_is_pd_author
def metology_pd_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        precipitation_dailynew = precipitation_daily.objects.filter(pk=id).first()
        form = precipitation_dailyForm(instance=precipitation_dailynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/pd_form.html', context)
    elif request.method == "POST":

        precipitation_dailynew = precipitation_daily.objects.filter(pk=id).first()
        form = precipitation_dailyForm(request.POST, instance=precipitation_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')

            return redirect('pd-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('pd-list', id_field)


@login_required
@user_is_pd_author
def metology_pd_delete(request, id_field, id):
    deleted_precipitation_daily = precipitation_daily.objects.get(pk=id)
    deleted_precipitation_daily.delete()
    messages.success(request, 'the deleted done successfully')

    return redirect('pd-list', id_field)

@login_required
@user_is_pd_author
def metology_pd_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    precipitation_dailys = xy_metology.precipitation_dailys.filter(waterpoint_id=id_field)
    precipitation_dailys = filter_precipitation_daily(precipitation_dailys, paramDict)

    paramDict = request.GET
    precipitation_dailys = filter_precipitation_daily(precipitation_dailys, paramDict)
    for precipitation_daily in precipitation_dailys:
        precipitation_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('pd-list', id_field)


@login_required
def export_precipitation_daily(request, id_field):
    precipitation_daily_resource = precipitation_dailyResource()
    paramDict = request.GET
    precipitation_dailys = precipitation_daily.objects.filter(waterpoint_id=id_field)
    precipitation_dailys = filter_precipitation_daily(precipitation_dailys, paramDict)

    dataset = precipitation_daily_resource.export(precipitation_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="precipitation_daily.xls"'
    return response

@login_required
def pd_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    precipitation_dailys = xy_metology.precipitation_dailys.filter(created_by=request.user)

    paramDict = request.GET
    precipitation_dailys_new = filter_precipitation_daily(precipitation_dailys, paramDict)

    x = list()
    for entry in precipitation_dailys_new:
        x.append(entry.prcp_mm)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'precipitation_dailys_new': precipitation_dailys_new,
        'xy_metology_information': xy_metology_information,
        'count_x': count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/pd_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start precipitation_monthly #########
@login_required
def metology_pm_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    precipitation_monthlys = xy_metology.precipitation_monthlys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    precipitation_monthlys_new = filter_precipitation_monthly(precipitation_monthlys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'xy_metology': xy_metology,
        'precipitation_monthlys_new': precipitation_monthlys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date
    }
    return render(request, 'observe/metology/metology_pm_list.html', context)


@login_required
def metology_pm_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = precipitation_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('pm-list', id_field)
        else:
            messages.warning(request, 'sorry the  added failed')
            return redirect('pm-list', id_field)

    elif (request.method == "GET"):
        form = precipitation_monthlyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/pm_form.html', context)


@login_required
@user_is_pm_author
def metology_pm_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        precipitation_monthlynew = precipitation_monthly.objects.filter(pk=id).first()
        form = precipitation_monthlyForm(instance=precipitation_monthlynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/pm_form.html', context)
    elif request.method == "POST":

        precipitation_monthlynew = precipitation_monthly.objects.filter(pk=id).first()
        form = precipitation_monthlyForm(request.POST, instance=precipitation_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('pm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('pm-list', id_field)


@login_required
@user_is_pm_author
def metology_pm_delete(request, id_field, id):
    deleted_precipitation_monthly = precipitation_monthly.objects.get(pk=id)
    deleted_precipitation_monthly.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('pm-list', id_field)

@login_required
@user_is_pm_author
def metology_pm_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    precipitation_monthlys = xy_metology.precipitation_monthlys.filter(waterpoint_id=id_field)
    precipitation_monthlys = filter_precipitation_monthly(precipitation_monthlys, paramDict)

    paramDict = request.GET
    precipitation_monthlys = filter_precipitation_monthly(precipitation_monthlys, paramDict)
    for precipitation_monthly in precipitation_monthlys:
        precipitation_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('pm-list', id_field)

@login_required
def export_precipitation_monthly(request, id_field):
    precipitation_monthly_resource = precipitation_monthlyResource()
    paramDict = request.GET
    precipitation_monthlys = precipitation_monthly.objects.filter(waterpoint_id=id_field)
    precipitation_monthlys = filter_precipitation_monthly(precipitation_monthlys, paramDict)

    dataset = precipitation_monthly_resource.export(precipitation_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="precipitation_monthly.xls"'
    return response

@login_required
def pm_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    precipitation_monthlys = xy_metology.precipitation_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    precipitation_monthlys_new = filter_precipitation_monthly(precipitation_monthlys, paramDict)
    x = list()
    for entry in precipitation_monthlys_new:
        x.append(entry.monthly_precipitaion)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'precipitation_monthlys_new': precipitation_monthlys_new,
        'xy_metology_information': xy_metology_information,
        'mean_x': mean_x,
        'max_x': max_x,
        'min_x': min_x,
        'count_x': count_x,

        'xy_metology': xy_metology,

    }
    pdf = render_to_pdf('observe/metology/pm_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start precipitation_annual #########

@login_required
def metology_pa_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    precipitation_annuals = xy_metology.precipitation_annuals.filter(created_by=request.user)
    form_date = QueryAnuallDateForm(request.GET or None)
    paramDict = request.GET
    precipitation_annuals_new = filter_precipitation_annual(precipitation_annuals, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'precipitation_annuals_new': precipitation_annuals_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology
    }
    return render(request, 'observe/metology/metology_pa_list.html', context)


@login_required
def metology_pa_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = precipitation_annualForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('pa-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('pa-list', id_field)

    elif (request.method == "GET"):
        form = precipitation_annualForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/pa_form.html', context)


@login_required
@user_is_pa_author
def metology_pa_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        precipitation_annualnew = precipitation_annual.objects.filter(pk=id).first()
        form = precipitation_annualForm(instance=precipitation_annualnew)

        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/pa_form.html', context)
    elif request.method == "POST":

        precipitation_annualnew = precipitation_annual.objects.filter(pk=id).first()
        form = precipitation_annualForm(request.POST, instance=precipitation_annualnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')

            return redirect('pa-list', id_field)
        else:
            messages.warning(request, 'the updated failed ')

            return redirect('pa-list', id_field)


@login_required
@user_is_pa_author
def metology_pa_delete(request, id_field, id):
    deleted_precipitation_annual = precipitation_annual.objects.get(pk=id)
    deleted_precipitation_annual.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('pa-list', id_field)

@login_required
@user_is_pa_author
def metology_pa_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    precipitation_annuals = xy_metology.precipitation_annuals.filter(waterpoint_id=id_field)
    precipitation_annuals = filter_precipitation_annual(precipitation_annuals, paramDict)

    paramDict = request.GET
    precipitation_annuals = filter_precipitation_annual(precipitation_annuals, paramDict)
    for precipitation_annual in precipitation_annuals:
        precipitation_annual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('pa-list', id_field)


@login_required
def export_precipitation_annual(request, id_field):
    precipitation_annual_resource = precipitation_annualResource()
    paramDict = request.GET
    precipitation_annuals = precipitation_annual.objects.filter(waterpoint_id=id_field)
    precipitation_annuals = filter_precipitation_annual(precipitation_annuals, paramDict)

    dataset = precipitation_annual_resource.export(precipitation_annuals)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="precipitation_annual.xls"'
    return response

@login_required
def pa_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    precipitation_annuals = xy_metology.precipitation_annuals.filter(created_by=request.user)

    paramDict = request.GET
    precipitation_annuals_new = filter_precipitation_annual(precipitation_annuals, paramDict)

    x = list()
    for entry in precipitation_annuals_new:
        x.append(entry.annual_precipitation)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'precipitation_annuals_new': precipitation_annuals_new,
        'mean_x': mean_x,
        'xy_metology_information': xy_metology_information,
        'xy_metology': xy_metology,
        'count_x': count_x,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,

    }
    pdf = render_to_pdf('observe/metology/pa_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

#####################start snowfall #########
@login_required
def metology_snowfall_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    snowfalls = xy_metology.snowfalls.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    snowfalls_new = filter_snowfall(snowfalls, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'snowfalls_new': snowfalls_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology
    }
    return render(request, 'observe/metology/metology_snowfall_list.html', context)


@login_required
def metology_snowfall_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = snowfallForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('snowfall-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('snowfall-list', id_field)

    elif (request.method == "GET"):
        form = snowfallForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/snowfall_form.html', context)


@login_required
@user_is_snowfall_author
def metology_snowfall_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        snowfallnew = snowfall.objects.filter(pk=id).first()
        form = snowfallForm(instance=snowfallnew)

        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/snowfall_form.html', context)
    elif request.method == "POST":

        snowfallnew = snowfall.objects.filter(pk=id).first()
        form = snowfallForm(request.POST, instance=snowfallnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')

            return redirect('snowfall-list', id_field)
        else:
            messages.warning(request, 'the updated failed ')

            return redirect('snowfall-list', id_field)


@login_required
@user_is_snowfall_author
def metology_snowfall_delete(request, id_field, id):
    deleted_snowfall = snowfall.objects.get(pk=id)
    deleted_snowfall.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('snowfall-list', id_field)
@login_required
@user_is_snowfall_author
def metology_snowfall_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    snowfalls = xy_metology.snowfalls.filter(waterpoint_id=id_field)
    snowfalls = filter_snowfall(snowfalls, paramDict)

    paramDict = request.GET
    snowfalls = filter_snowfall(snowfalls, paramDict)
    for snowfall in snowfalls:
        snowfall.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('snowfall-list', id_field)

@login_required
def export_snowfall(request, id_field):
    snowfall_resource = snowfallResource()
    paramDict = request.GET
    snowfalls = snowfall.objects.filter(waterpoint_id=id_field)
    snowfalls = filter_snowfall(snowfalls, paramDict)

    dataset = snowfall_resource.export(snowfalls)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="snowfall.xls"'
    return response

@login_required
def snowfall_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    snowfalls = xy_metology.snowfalls.filter(created_by=request.user)

    paramDict = request.GET
    snowfalls_new = filter_snowfall(snowfalls, paramDict)

    x = list()
    for entry in snowfalls_new:
        x.append(entry.dailysnowfall)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'snowfalls_new': snowfalls_new,
        'mean_x': mean_x,
        'xy_metology_information': xy_metology_information,
        'xy_metology': xy_metology,
        'count_x': count_x,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,

    }
    pdf = render_to_pdf('observe/metology/snowfall_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

#####################start snowdepth #########
@login_required
def metology_snowdepth_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    snowdepths = xy_metology.snowdepths.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    snowdepths_new = filter_snowdepth(snowdepths, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'snowdepths_new': snowdepths_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology
    }
    return render(request, 'observe/metology/metology_snowdepth_list.html', context)


@login_required
def metology_snowdepth_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = snowdepthForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('snowdepth-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('snowdepth-list', id_field)

    elif (request.method == "GET"):
        form = snowdepthForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/snowdepth_form.html', context)


@login_required
@user_is_snowdepth_author
def metology_snowdepth_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        snowdepthnew = snowdepth.objects.filter(pk=id).first()
        form = snowdepthForm(instance=snowdepthnew)

        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/snowdepth_form.html', context)
    elif request.method == "POST":

        snowdepthnew = snowdepth.objects.filter(pk=id).first()
        form = snowdepthForm(request.POST, instance=snowdepthnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')

            return redirect('snowdepth-list', id_field)
        else:
            messages.warning(request, 'the updated failed ')

            return redirect('snowdepth-list', id_field)


@login_required
@user_is_snowdepth_author
def metology_snowdepth_delete(request, id_field, id):
    deleted_snowdepth = snowdepth.objects.get(pk=id)
    deleted_snowdepth.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('snowdepth-list', id_field)

@login_required
@user_is_snowdepth_author
def metology_snowdepth_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    snowdepths = xy_metology.snowdepths.filter(waterpoint_id=id_field)
    snowdepths = filter_snowdepth(snowdepths, paramDict)

    paramDict = request.GET
    snowdepths = filter_snowdepth(snowdepths, paramDict)
    for snowdepth in snowdepths:
        snowdepth.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('snowdepth-list', id_field)

@login_required
def export_snowdepth(request, id_field):
    snowdepth_resource = snowfallResource()
    paramDict = request.GET
    snowdepths = snowdepth.objects.filter(waterpoint_id=id_field)
    snowdepths = filter_snowdepth(snowdepths, paramDict)

    dataset = snowdepth_resource.export(snowdepths)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="snowdepth.xls"'
    return response

@login_required
def snowdepth_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    snowdepths = xy_metology.snowdepths.filter(created_by=request.user)

    paramDict = request.GET
    snowdepths_new = filter_snowdepth(snowdepths, paramDict)

    x = list()
    for entry in snowdepths_new:
        x.append(entry.dailysnowdepth)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'snowdepths_new': snowdepths_new,
        'mean_x': mean_x,
        'xy_metology_information': xy_metology_information,
        'xy_metology': xy_metology,
        'count_x': count_x,
        'max_x': max_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,

    }
    pdf = render_to_pdf('observe/metology/snowdepth_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

#####################start wind_daily #########
@login_required
def metology_wd_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    wind_dailys = xy_metology.wind_dailys.filter(created_by=request.user)

    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    wind_dailys_new = filter_wind_daily(wind_dailys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'xy_metology': xy_metology,
        'wind_dailys_new': wind_dailys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date
    }
    return render(request, 'observe/metology/metology_wd_list.html', context)


@login_required
def metology_wd_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = wind_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('wd-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('wd-list', id_field)

    elif (request.method == "GET"):
        form = wind_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/wd_form.html', context)


@login_required
@user_is_wd_author
def metology_wd_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        wind_dailynew = wind_daily.objects.filter(pk=id).first()
        form = wind_dailyForm(instance=wind_dailynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/wd_form.html', context)
    elif request.method == "POST":

        wind_dailynew = wind_daily.objects.filter(pk=id).first()
        form = wind_dailyForm(request.POST, instance=wind_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('wd-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('wd-list', id_field)


@login_required
@user_is_wd_author
def metology_wd_delete(request, id_field, id):
    deleted_wind_daily = wind_daily.objects.get(pk=id)
    deleted_wind_daily.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('wd-list', id_field)

@login_required
@user_is_wd_author
def metology_wd_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    wind_dailys = xy_metology.wind_dailys.filter(waterpoint_id=id_field)
    wind_dailys = filter_wind_daily(wind_dailys, paramDict)

    paramDict = request.GET
    wind_dailys = filter_wind_daily(wind_dailys, paramDict)
    for wind_daily in wind_dailys:
        wind_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('wd-list', id_field)




@login_required
def export_wind_daily(request, id_field):
    wind_daily_resource = wind_dailyResource()
    paramDict = request.GET
    wind_dailys = wind_daily.objects.filter(waterpoint_id=id_field)
    wind_dailys = filter_wind_daily(wind_dailys, paramDict)

    dataset = wind_daily_resource.export(wind_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="wind_daily.xls"'
    return response


@login_required
def wd_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    wind_dailys = xy_metology.wind_dailys.filter(created_by=request.user)

    paramDict = request.GET
    wind_dailys_new = filter_wind_daily(wind_dailys, paramDict)

    x = list()
    for entry in wind_dailys_new:
        x.append(entry.daily_avg)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'wind_dailys_new': wind_dailys_new,
        'xy_metology_information':xy_metology_information,
        'count_x' :count_x,
        'mean_x': mean_x,
        'xy_metology': xy_metology,
        'max_x': max_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x
    }
    pdf = render_to_pdf('observe/metology/wd_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
def wd_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    wind_dailys = xy_metology.wind_dailys.filter(created_by=request.user)

    paramDict = request.GET
    wind_dailys_new = filter_wind_daily(wind_dailys, paramDict)

    x = list()
    for entry in wind_dailys_new:
        x.append(entry.daily_max)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    count_x = len(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'wind_dailys_new': wind_dailys_new,
        'xy_metology_information':xy_metology_information,
        'count_x':count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/wd_max_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
def wd_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    wind_dailys = xy_metology.wind_dailys.filter(created_by=request.user)

    paramDict = request.GET
    wind_dailys_new = filter_wind_daily(wind_dailys, paramDict)

    x = list()
    for entry in wind_dailys_new:
        x.append(entry.daily_min)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    count_x=len(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'wind_dailys_new': wind_dailys_new,
        'xy_metology_information':xy_metology_information,
        'count_x':count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/wd_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start wind_monthly #########
@login_required
def metology_wm_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()
    xy_metology_information = xy_metology.metology_inf

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    wind_monthlys = xy_metology.wind_monthlys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    wind_monthlys_new = filter_wind_monthly(wind_monthlys, paramDict)
    x = list()


    context = {
        'metologyinfnew': metologyinfnew,
        'wind_monthlys_new': wind_monthlys_new,
        'id_field': id_field,
        'xy_metology': xy_metology,

        'map_xy_metology': map_xy_metology,
        'form_date': form_date
    }
    return render(request, 'observe/metology/metology_wm_list.html', context)


@login_required
def metology_wm_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = wind_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully')
            return redirect('wm-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('wm-list', id_field)


    elif (request.method == "GET"):
        form = wind_monthlyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/wm_form.html', context)


@login_required
@user_is_wm_author
def metology_wm_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        wind_monthlynew = wind_monthly.objects.filter(pk=id).first()
        form = wind_monthlyForm(instance=wind_monthlynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/wm_form.html', context)
    elif request.method == "POST":

        wind_monthlynew = wind_monthly.objects.filter(pk=id).first()
        form = wind_monthlyForm(request.POST, instance=wind_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')

            return redirect('wm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')

            return redirect('wm-list', id_field)


@login_required
@user_is_wm_author
def metology_wm_delete(request, id_field, id):
    deleted_wind_monthly = wind_monthly.objects.get(pk=id)
    deleted_wind_monthly.delete()
    messages.success(request, 'the deleted done successfully')

    return redirect('wm-list', id_field)

def metology_wm_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    wind_monthlys = xy_metology.wind_monthlys.filter(waterpoint_id=id_field)
    wind_monthlys = filter_wind_daily(wind_monthlys, paramDict)

    paramDict = request.GET
    wind_monthlys = filter_wind_daily(wind_monthlys, paramDict)
    for wind_monthly in wind_monthlys:
        wind_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('wm-list', id_field)



@login_required
def export_wind_monthly(request, id_field):
    wind_monthly_resource = wind_monthlyResource()
    paramDict = request.GET
    wind_monthlys = wind_monthly.objects.filter(waterpoint_id=id_field)
    wind_monthlys = filter_wind_monthly(wind_monthlys, paramDict)

    dataset = wind_monthly_resource.export(wind_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="wind_monthly.xls"'
    return response


@login_required
def wm_avg_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    wind_monthlys = xy_metology.wind_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    wind_monthlys_new = filter_wind_daily(wind_monthlys, paramDict)

    x = list()
    for entry in wind_monthlys_new:
        x.append(entry.avg_monthly_wind_from_hour)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'wind_monthlys_new': wind_monthlys_new,
        'xy_metology_information':xy_metology_information,
        'mean_x': mean_x,
'count_x':count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/wm_avg_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#####################start sunshine daily #########

@login_required
def metology_sd_list(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    metologyinfnew = Metology_inf.objects.filter(xy_metology=xy_metology.pk).first()

    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))

    sunshine_dailys = xy_metology.sunshine_dailys.filter(created_by=request.user)
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    sunshine_dailys_new = filter_sunshine_daily(sunshine_dailys, paramDict)
    context = {
        'metologyinfnew': metologyinfnew,
        'sunshine_dailys_new': sunshine_dailys_new,
        'id_field': id_field,
        'map_xy_metology': map_xy_metology,
        'form_date': form_date,
        'xy_metology': xy_metology,
    }
    return render(request, 'observe/metology/metology_sd_list.html', context)


@login_required
def metology_sd_create_form(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if (request.method == "POST"):
        form = sunshine_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_metology
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added  successfully')

            return redirect('sd-list', id_field)
        else:
            messages.warning(request, 'sorry the added  failed')
            return redirect('sd-list', id_field)


    elif (request.method == "GET"):
        form = sunshine_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/metology/sd_form.html', context)


@login_required
@user_is_sd_author
def metology_sd_update_form(request, id_field, id):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    if request.method == "GET":
        sunshine_dailynew = sunshine_daily.objects.filter(pk=id).first()
        form = sunshine_dailyForm(instance=sunshine_dailynew)
        context = {'form': form, 'id_field': id_field}
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/metology/sd_form.html', context)
    elif request.method == "POST":

        sunshine_dailynew = sunshine_daily.objects.filter(pk=id).first()
        form = sunshine_dailyForm(request.POST, instance=sunshine_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done  successfully')

            return redirect('sd-list', id_field)
        else:
            messages.warning(request, 'sorry updated failed')
            return redirect('sd-list', id_field)


@login_required
@user_is_sd_author
def metology_sd_delete(request, id_field, id):
    deleted_sunshine_daily = sunshine_daily.objects.get(pk=id)
    deleted_sunshine_daily.delete()
    messages.success(request, 'the deleted done  successfully')

    return redirect('sd-list', id_field)



@login_required

@user_is_sd_author
def metology_sd_multi_delete(request,id_field):
    paramDict = request.GET
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    sunshine_dailys = xy_metology.sunshine_dailys.filter(waterpoint_id=id_field)
    sunshine_dailys = filter_sunshine_daily(sunshine_dailys, paramDict)

    paramDict = request.GET
    sunshine_dailys = filter_sunshine_daily(sunshine_dailys, paramDict)
    for sunshine_daily in sunshine_dailys:
        sunshine_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sd-list', id_field)

@login_required        
def export_sunshine_daily(request, id_field):
    sunshine_daily_resource = sunshine_dailyResource()
    paramDict = request.GET
    sunshine_dailys = sunshine_daily.objects.filter(waterpoint_id=id_field)
    sunshine_dailys = filter_sunshine_daily(sunshine_dailys, paramDict)

    dataset = sunshine_daily_resource.export(sunshine_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sunshine_daily.xls"'
    return response


def sd_rad_max_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    sunshine_dailys = xy_metology.sunshine_dailys.filter(created_by=request.user)

    paramDict = request.GET
    sunshine_dailys_new = filter_sunshine_daily(sunshine_dailys, paramDict)

    x = list()
    for entry in sunshine_dailys_new:
        x.append(entry.rad_max_w_m2)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'sunshine_dailys_new': sunshine_dailys_new,
        'mean_x': mean_x,
'xy_metology_information':xy_metology_information,
        'xy_metology': xy_metology,
'count_x' :count_x   ,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/sh_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


def sd_rad_min_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    sunshine_dailys = xy_metology.sunshine_dailys.filter(created_by=request.user)

    paramDict = request.GET
    sunshine_dailys_new = filter_sunshine_daily(sunshine_dailys, paramDict)

    x = list()
    for entry in sunshine_dailys_new:
        x.append(entry.rad_min_w_m2)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'sunshine_dailys_new': sunshine_dailys_new,
        'mean_x': mean_x,
'xy_metology_information':xy_metology_information,
        'count_x':count_x,
        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/sd_rad_min_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


def sd_rad_mj_Pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)
    map_xy_metology = serialize('geojson', XY_Metology.objects.filter(pk=id_field))
    xy_metology_information = xy_metology.metology_inf
    id_field = xy_metology.id_field
    sunshine_dailys = xy_metology.sunshine_dailys.filter(created_by=request.user)

    paramDict = request.GET
    sunshine_dailys_new = filter_sunshine_daily(sunshine_dailys, paramDict)

    x = list()
    for entry in sunshine_dailys_new:
        x.append(entry.rad_mj_m2)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'sunshine_dailys_new': sunshine_dailys_new,
        'xy_metology_information':xy_metology_information,
        'count_x':count_x,
        'mean_x': mean_x,

        'xy_metology': xy_metology,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/metology/sd_rad_mj_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


def export_filtered_metologys_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="waterpoints.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
         'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x', 'stm_y'])
    waterpoints = XY_Metology.objects.all()
    paramDict = request.GET
    waterpoints = filter_waterpoints(waterpoints, paramDict)
    waterpoints = waterpoints.values_list(
        'id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
        'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x', 'stm_y')

    for waterpoint in waterpoints:
        writer.writerow(waterpoint)

    return response


def export_filtered_metologys_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="waterpoints.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('waterpoints')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia',
               'village',
               'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x', 'stm_y']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = XY_Metology.objects.all().values_list('id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency',
                                                 'mohafaza', 'montika', 'nahia', 'village',
                                                 'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x',
                                                 'stm_y')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


#####################################33333
def drawMyRuler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')


from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.conf import settings
import os


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path


from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors


def generate_pdf(request, id_field):
    xy_metology = get_object_or_404(XY_Metology, pk=id_field)

    image = fetch_resources(xy_metology.image.url, xy_metology.image.url)
    data = [
        ['Dedicated Hosting', 'VPS Hosting', 'Sharing Hosting', 'Reseller Hosting'],
        ['€200/Month', '€100/Month', '€20/Month', '€50/Month'],
        ['Free Domain', 'Free Domain', 'Free Domain', 'Free Domain'],
        ['2GB DDR2', '20GB Disc Space', 'Unlimited Email', 'Unlimited Email']
    ]
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 2, colors.black),

            ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

            ('GRID', (0, 1), (-1, -1), 2, colors.black),
        ]
    )
    table.setStyle(ts)
    elems = []
    elems.append(table)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    drawMyRuler(p)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawString(100, 100, "mohafaza : ." + str(xy_metology.mohafaza))
    p.drawString(100, 200, "montika" + str(xy_metology.montika))
    p.drawString(100, 300, "Point Coordinate" + str(xy_metology.geom))
    p.drawInlineImage(image, 150, 600)
    p.build(elems)

    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

########################3
