from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import statistics
import scipy.stats
from django.utils import timezone
from observe.utils.utils import render_to_pdf
from observe.rivers.models import riverdischarge_daily, XY_River, riverdischarge_monthly, riverdischarge_anual, \
    riverflowmeasure, discharge_survey, sectionareasurvey, sectiondata, surface_hq, River_inf
from observe.rivers.forms import RiverForm, River_infForm
from observe.models import Waterpoint
# from observe.springs.models import XY_Spring
from observe.forms import QueryForm, QueryDateForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views import generic
from observe.rivers.resources import riverdischarge_anualResource, riverdischarge_dailyResource, \
    riverdischarge_monthlyResource, riverflowmeasureResource, \
    sectiondataResource, discharge_surveyResource, sectionareasurveyResource, surface_hqResource
from observe.rivers.filter import filter_discharge_survey, filter_riverdischarge_anual, \
    filter_riverdischarge_monthly, filter_riverflowmeasure, filter_riverdischarge_daily,\
    filter_sectionareasurvey, filter_sectiondata, filter_surface_hq,filter_riverdischarge_daily
from observe.rivers.decorators import user_is_riverdischarge_anual_author, user_is_riverdischarge_monthly_author, \
    user_is_riverdischarge_daily_author, \
    user_is_riverflowmeasure_author, user_is_surface_hq_author, user_is_discharge_survey_author, \
    user_is_sectionareasurvey_author, user_is_sectiondata_author
##########################
from django.utils.safestring import SafeString
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.gis.serializers import geojson
from django.contrib import messages

from django.urls import reverse

from observe.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView

from django.http import JsonResponse
from django.template.loader import render_to_string
############
from observe.rivers.forms import riverdischarge_monthlyForm, riverdischarge_anualForm, riverdischarge_dailyForm, \
    riverflowmeasureForm, discharge_surveyForm, sectionareasurveyForm, sectiondataForm, surface_hqForm, \
    riverflowmeasureForm
from observe.utils.filter import filter_waterpoints, filter_date
import tablib
from observe.Resources import River_dis_dailyResource
import csv
import xlwt


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'observe/index.html'


################33

class RiverListView(BaseListView):
    model = XY_River
    paginate_by = 100  # if pagination is desired


class RiverCreate(LoginRequiredMixin, BaseCreateView):
    model = XY_River
    form_class = RiverForm

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        created_by = self.request.user
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'Your point was  saved successfully!')
        return super().form_valid(form)


class RiverUpdate(LoginRequiredMixin, BaseUpdateView):
    model = XY_River
    form_class = RiverForm
    template_name = 'observe/river_form.html'

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Your point was  updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        xy_river = self.get_object()
        if self.request.user == xy_river.created_by:
            return True
        else:
            return False


class RiverDelete(LoginRequiredMixin, UserPassesTestMixin, BaseDeleteView):
    model = XY_River
    success_url = '/xy_metologys'

    # def get_success_url(self):
    #     return reverse('/xy_rivers')
    def test_func(self):
        xy_river = self.get_object()
        if self.request.user == xy_river.created_by:
            return True
        else:
            return False


################ River_inf
def river_inf_update_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()
    if request.method == "GET":
        form = River_infForm(instance=riverinfnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/riverinf_form.html', context)
    elif request.method == "POST":

        form = River_infForm(request.POST, instance=riverinfnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('xy_rivers')


#########3


def waterpoints_datasets(request):
    points = serialize('geojson', Waterpoint.objects.all())
    return HttpResponse(points, content_type='json')


def xy_river_datasets(request):
    river_points = serialize('geojson', XY_River.objects.all())
    return HttpResponse(river_points, content_type='json')


def all_xy_rivers(request):
    XY_Rivers = XY_River.objects.all()
    form = QueryForm(request.GET or None)
    paramDict = request.GET
    XY_Rivers = filter_waterpoints(XY_Rivers, paramDict)
    map_XY_Rivers = serialize('geojson', XY_Rivers)

    print(map_XY_Rivers)
    context = {
        'XY_Rivers': XY_Rivers,
        'map_XY_Rivers': map_XY_Rivers,
        'form': form,
    }
    return render(request, 'observe/river.html', context)


def import_river_readings(request):
    XY_Rivers = XY_River.objects.all()

    map_XY_Rivers= serialize('geojson', XY_Rivers)


    context = {
        'XY_Rivers': XY_Rivers,
        'map_XY_Rivers': map_XY_Rivers,

    }
    return render(request,'observe/river_import_form.html',context)



##################### start river_discharge_daily#############
@login_required
def river_rdd_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    ###########riverdischarge_dailys###############
    riverdischarge_dailys = xy_river.riverdischarge_dailys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    riverdischarge_dailys_new = filter_date(riverdischarge_dailys, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'riverdischarge_dailys_new': riverdischarge_dailys_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date,
        'xy_river': xy_river
    }
    return render(request, 'observe/river/river_rdd_list.html', context)


@login_required
def river_rdd_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = riverdischarge_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('rdd-list', id_field)
        else:
            messages.warning(request, 'sorry the added faild!')
            return redirect('rdd-list', id_field)

    elif (request.method == "GET"):
        form = riverdischarge_dailyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rdd_form.html', context)


@login_required
@user_is_riverdischarge_daily_author
def river_rdd_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        riverdischarge_dailynew = riverdischarge_daily.objects.filter(pk=id).first()
        form = riverdischarge_dailyForm(instance=riverdischarge_dailynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rdd_form.html', context)
    elif request.method == "POST":

        riverdischarge_dailynew = riverdischarge_daily.objects.filter(pk=id).first()
        form = riverdischarge_dailyForm(request.POST, instance=riverdischarge_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('rdd-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('rdd-list', id_field)


@login_required
@user_is_riverdischarge_daily_author
def river_rdd_delete(request, id_field, id):
    deleted_riverdischarge_daily = riverdischarge_daily.objects.get(pk=id)
    deleted_riverdischarge_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rdd-list', id_field)

@login_required
@user_is_riverdischarge_daily_author
def river_rdd_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverdischarge_dailys = xy_river.riverdischarge_dailys.filter(waterpoint_id=id_field)
    riverdischarge_dailys = filter_riverdischarge_monthly(riverdischarge_dailys, paramDict)

    paramDict = request.GET
    filter_riverdischarge_dailys = filter_riverdischarge_monthly(riverdischarge_dailys, paramDict)
    for filter_riverdischarge_daily in filter_riverdischarge_dailys:
        filter_riverdischarge_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rdd-list', id_field)


@login_required
def export_river_discharge_daily(request, id_field):
    riverdischarge_daily_resource = riverdischarge_dailyResource()
    paramDict = request.GET
    riverdischarge_dailys = riverdischarge_daily.objects.filter(waterpoint_id=id_field)
    riverdischarge_dailys = filter_riverdischarge_daily(riverdischarge_dailys, paramDict)
    dataset = riverdischarge_daily_resource.export(riverdischarge_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="river_dischrge_daily.xls"'
    return response

@login_required
def river_rdd_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    riverdischarge_dailys_new = xy_river.riverdischarge_dailys.filter(created_by=request.user)

    paramDict = request.GET
    riverdischarge_dailys_new = filter_riverdischarge_daily(riverdischarge_dailys_new, paramDict)

    x = list()
    for entry in riverdischarge_dailys_new:
        x.append(entry.discharge_m3_sec)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'riverdischarge_dailys_new': riverdischarge_dailys_new,
        'mean_x': mean_x,
'count_x':count_x,
        'xy_river_inf' : xy_river_inf,
        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rdd_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#########start river_discharge_monthly###########
@login_required
def river_rdm_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))

    riverdischarge_monthlys = xy_river.riverdischarge_monthlys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    riverdischarge_monthlys_new = filter_riverdischarge_monthly(riverdischarge_monthlys, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'riverdischarge_monthlys_new': riverdischarge_monthlys_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date,
        'xy_river': xy_river,
    }
    return render(request, 'observe/river/river_rdm_list.html', context)


@login_required
def river_rdm_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = riverdischarge_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('rdm-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')

    elif (request.method == "GET"):
        form = riverdischarge_monthlyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rdm_form.html', context)


@login_required
@user_is_riverdischarge_monthly_author
def river_rdm_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        riverdischarge_monthlynew = riverdischarge_monthly.objects.filter(pk=id).first()
        form = riverdischarge_monthlyForm(instance=riverdischarge_monthlynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rdm_form.html', context)
    elif request.method == "POST":

        riverdischarge_monthlynew = riverdischarge_monthly.objects.filter(pk=id).first()
        form = riverdischarge_monthlyForm(request.POST, instance=riverdischarge_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('rdm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed !')
            return redirect('rdm-list', id_field)


@login_required
@user_is_riverdischarge_monthly_author
def river_rdm_delete(request, id_field, id):
    deleted_riverdischarge_daily = riverdischarge_monthly.objects.get(pk=id)
    deleted_riverdischarge_daily.delete()
    messages.success(request, 'the deleted done successfuly!')
    return redirect('rdm-list', id_field)

@login_required
@user_is_riverdischarge_monthly_author
def river_discharge_monthly_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverdischarge_monthlys = xy_river.riverdischarge_monthlys.filter(waterpoint_id=id_field)
    riverdischarge_monthlys = filter_riverdischarge_monthly(riverdischarge_monthlys, paramDict)

    paramDict = request.GET
    riverdischarge_monthlys = filter_riverdischarge_monthly(riverdischarge_monthlys, paramDict)
    for riverdischarge_monthly in riverdischarge_monthlys:
        riverdischarge_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rdm-list', id_field)


@login_required
def export_river_discharge_monthly(request, id_field):
    riverdischarge_monthly_resource = riverdischarge_monthlyResource()
    paramDict = request.GET
    riverdischarge_monthlys = riverdischarge_monthly.objects.filter(waterpoint_id=id_field)
    riverdischarge_monthlys = filter_riverdischarge_monthly(riverdischarge_monthlys, paramDict)

    dataset = riverdischarge_monthly_resource.export(riverdischarge_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="riverdischarge_monthly.xls"'
    return response

@login_required
def river_rdm_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    riverdischarge_monthlys_new = xy_river.riverdischarge_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    riverdischarge_monthlys_new = filter_riverdischarge_monthly(riverdischarge_monthlys_new, paramDict)

    x = list()
    for entry in riverdischarge_monthlys_new:
        x.append(entry.monthly_avg_discharge)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    count_x=len(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'riverdischarge_monthlys_new': riverdischarge_monthlys_new,
        'xy_river_inf':xy_river_inf,
        'mean_x': mean_x,
'count_x':count_x,
        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rdm_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


######################start river discharge annual #########
@login_required
def river_rda_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))

    riverdischarge_anuals = xy_river.riverdischarge_anuals.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    riverdischarge_anuals_new = filter_date(riverdischarge_anuals, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'riverdischarge_anuals_new': riverdischarge_anuals_new,
        'id_field': id_field,
        'xy_river': xy_river,
        'map_xy_river': map_xy_river,
        'form_date': form_date
    }
    return render(request, 'observe/river/river_rda_list.html', context)


@login_required
def river_rda_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = riverdischarge_anualForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading added successfully!')
            return redirect('rda-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('rda-list', id_field)


    elif (request.method == "GET"):
        form = riverdischarge_anualForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rda_form.html', context)


@login_required
@user_is_riverdischarge_anual_author
def river_rda_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        riverdischarge_anualnew = riverdischarge_anual.objects.filter(pk=id).first()
        form = riverdischarge_anualForm(instance=riverdischarge_anualnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rda_form.html', context)
    elif request.method == "POST":

        riverdischarge_anualnew = riverdischarge_anual.objects.filter(pk=id).first()
        form = riverdischarge_anualForm(request.POST, instance=riverdischarge_anualnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully')
            return redirect('rda-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('rda-list', id_field)

@login_required
@user_is_riverdischarge_anual_author
def river_rda_delete(request, id_field, id):
    deleted_riverdischarge_anual = riverdischarge_anual.objects.get(pk=id)
    deleted_riverdischarge_anual.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('rda-list', id_field)

@login_required
@user_is_riverdischarge_anual_author
def riverdischarge_anuall_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverdischarge_anuals = xy_river.riverdischarge_anuals.filter(waterpoint_id=id_field)
    riverdischarge_anuals = filter_riverdischarge_anual(riverdischarge_anuals, paramDict)

    paramDict = request.GET
    riverdischarge_anuals = filter_riverdischarge_anual(riverdischarge_anuals, paramDict)
    for riverdischarge_anual in riverdischarge_anuals:
        riverdischarge_anual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rda-list', id_field)


@login_required
def export_river_discharge_annual(request, id_field):
    riverdischarge_anual_resource = riverdischarge_anualResource()
    paramDict = request.GET
    riverdischarge_anuals = riverdischarge_anual.objects.filter(waterpoint_id=id_field)
    riverdischarge_anuals = filter_riverdischarge_anual(riverdischarge_anuals, paramDict)

    dataset = riverdischarge_anual_resource.export(riverdischarge_anuals)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="riverdischarge_anual.xls"'
    return response

@login_required
def river_rda_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    riverdischarge_anuals_new = xy_river.riverdischarge_anuals.filter(created_by=request.user)

    paramDict = request.GET
    riverdischarge_anuals_new = filter_riverdischarge_anual(riverdischarge_anuals_new, paramDict)

    x = list()
    for entry in riverdischarge_anuals_new:
        x.append(entry.anual_discharge)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'riverdischarge_anuals_new': riverdischarge_anuals_new,
        'mean_x': mean_x,
'xy_river_inf':xy_river_inf,
        'count_x':count_x,
        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rda_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


###################### start riverflowmeasure######
@login_required
def river_rfm_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    riverflowmeasures = xy_river.riverflowmeasures.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    riverflowmeasures_new = filter_riverflowmeasure(riverflowmeasures, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'riverflowmeasures_new': riverflowmeasures_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date,
        'xy_river': xy_river
    }
    return render(request, 'observe/river/river_rfm_list.html', context)


@login_required
def river_rfm_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = riverflowmeasureForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the added done successfully!')
            return redirect('rfm-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('rfm-list', id_field)

    elif (request.method == "GET"):
        form = riverflowmeasureForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rfm_form.html', context)


@login_required
@user_is_riverflowmeasure_author
def river_rfm_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        riverflowmeasurenew = riverflowmeasure.objects.filter(pk=id).first()
        form = riverflowmeasureForm(instance=riverflowmeasurenew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rfm_form.html', context)
    elif request.method == "POST":

        riverflowmeasurenew = riverflowmeasure.objects.filter(pk=id).first()
        form = riverflowmeasureForm(request.POST, instance=riverflowmeasurenew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('rfm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated faild!')
            return redirect('rfm-list', id_field)


@login_required
@user_is_riverflowmeasure_author
def river_rfm_delete(request, id_field, id):
    deleted_riverflowmeasure = riverflowmeasure.objects.get(pk=id)
    deleted_riverflowmeasure.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rfm-list', id_field)

@login_required
@user_is_riverflowmeasure_author
def riverflowmessure_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverflowmeasures = xy_river.riverflowmeasures.filter(waterpoint_id=id_field)
    riverflowmeasures = filter_riverflowmeasure(riverflowmeasures, paramDict)

    paramDict = request.GET
    riverflowmeasures = filter_riverflowmeasure(riverflowmeasures, paramDict)
    for riverflowmeasure in riverflowmeasures:
        riverflowmeasure.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rfm-list', id_field)


@login_required
def export_riverflowmeasure(request, id_field):
    riverflowmeasure_resource = riverflowmeasureResource()
    paramDict = request.GET
    riverflowmeasures = riverflowmeasure.objects.filter(waterpoint_id=id_field)
    riverflowmeasures = filter_riverflowmeasure(riverflowmeasures, paramDict)

    dataset = riverflowmeasure_resource.export(riverflowmeasures)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="riverflowmeasure.xls"'
    return response

@login_required
def river_rfm_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    riverflowmeasures = xy_river.riverflowmeasures.filter(created_by=request.user)

    paramDict = request.GET
    riverflowmeasures_new = filter_riverflowmeasure(riverflowmeasures, paramDict)
    x = list()
    for entry in riverflowmeasures_new:
        x.append(entry.avg_flow_velocity)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    count_x =len(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'riverflowmeasures_new': riverflowmeasures_new,
        'mean_x': mean_x,
        'xy_river': xy_river,
         'count_x': count_x,
        'xy_river_inf':xy_river_inf,
        'max_x': max_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
    }
    pdf = render_to_pdf('observe/river/rfm_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#########################surface_hq########
@login_required
def river_rhq_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))

    surface_hqs = xy_river.surface_hqs.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    surface_hqs_new = filter_date(surface_hqs, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'surface_hqs_new': surface_hqs_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date,
        'xy_river': xy_river
    }
    return render(request, 'observe/river/river_rhq_list.html', context)


@login_required
def river_rhq_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = surface_hqForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the added done successfully!')
            return redirect('rhq-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('rhq-list', id_field)

    elif (request.method == "GET"):
        form = surface_hqForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rhq_form.html', context)


@login_required
@user_is_surface_hq_author
def river_rhq_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        surface_hqnew = surface_hq.objects.filter(pk=id).first()
        form = surface_hqForm(instance=surface_hqnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rhq_form.html', context)
    elif request.method == "POST":

        surface_hqnew = surface_hq.objects.filter(pk=id).first()
        form = surface_hqForm(request.POST, instance=surface_hqnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('rhq-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed !')
            return redirect('rhq-list', id_field)


@user_is_surface_hq_author
def river_rhq_delete(request, id_field, id):
    deleted_surface_hq = surface_hq.objects.get(pk=id)
    deleted_surface_hq.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rhq-list', id_field)
@login_required
@user_is_surface_hq_author
def river_surface_hq_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    surface_hqs = xy_river.surface_hqs.filter(waterpoint_id=id_field)
    surface_hqs = filter_surface_hq(surface_hqs, paramDict)

    paramDict = request.GET
    surface_hqs = filter_surface_hq(surface_hqs, paramDict)
    for surface_hq in surface_hqs:
        surface_hq.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rhq-list', id_field)


@login_required
def export_surface_hq(request, id_field):
    surface_hq_resource = surface_hqResource()
    paramDict = request.GET
    surface_hqs = surface_hq.objects.filter(waterpoint_id=id_field)
    surface_hqs = filter_surface_hq(surface_hqs, paramDict)

    dataset = surface_hq_resource.export(surface_hqs)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="surface_hq.xls"'
    return response

@login_required
def river_rh_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    surface_hqs_new = xy_river.surface_hqs.filter(created_by=request.user)

    paramDict = request.GET
    surface_hqs_new = filter_surface_hq(surface_hqs_new, paramDict)

    x = list()
    for entry in surface_hqs_new:
        x.append(entry.h)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'surface_hqs_new': surface_hqs_new,
        'mean_x': mean_x,
        'xy_river_inf':xy_river_inf,
        'count_x':count_x,

        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rh_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
def river_rq_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    surface_hqs_new = xy_river.surface_hqs.filter(created_by=request.user)

    paramDict = request.GET
    surface_hqs_new = filter_surface_hq(surface_hqs_new, paramDict)

    x = list()
    for entry in surface_hqs_new:
        x.append(entry.q)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'surface_hqs_new': surface_hqs_new,
        'mean_x': mean_x,
'xy_river_inf':xy_river_inf,
        'count_x':count_x,
        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rq_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
def river_rvelocity_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    surface_hqs_new = xy_river.surface_hqs.filter(created_by=request.user)

    paramDict = request.GET
    surface_hqs_new = filter_surface_hq(surface_hqs_new, paramDict)

    x = list()
    for entry in surface_hqs_new:
        x.append(entry.velocity_m_s)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'surface_hqs_new': surface_hqs_new,
        'mean_x': mean_x,
        'xy_river_inf':xy_river_inf,
        'count_x':count_x,
        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rvelocity_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

###############discharge_survey##########
@login_required
def river_rds_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    discharge_surveys = xy_river.discharge_surveys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    discharge_surveys_new = filter_discharge_survey(discharge_surveys, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'discharge_surveys_new': discharge_surveys_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date,
        'xy_river': xy_river,
    }
    return render(request, 'observe/river/river_rds_list.html', context)


@login_required
def river_rds_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = discharge_surveyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the added done successfully!')
            return redirect('rds-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('rds-list', id_field)


    elif (request.method == "GET"):
        form = discharge_surveyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rds_form.html', context)


@login_required
@user_is_discharge_survey_author
def river_rds_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        discharge_surveynew = discharge_survey.objects.filter(pk=id).first()
        form = discharge_surveyForm(instance=discharge_surveynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rds_form.html', context)
    elif request.method == "POST":

        discharge_surveynew = discharge_survey.objects.filter(pk=id).first()
        form = discharge_surveyForm(request.POST, instance=discharge_surveynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('rds-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('rds-list', id_field)


@user_is_discharge_survey_author
def river_rds_delete(request, id_field, id):
    deleted_discharge_survey = discharge_survey.objects.get(pk=id)
    deleted_discharge_survey.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rds-list', id_field)

@login_required
@user_is_discharge_survey_author
def river_discharge_survey_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    discharge_surveys = xy_river.discharge_surveys.filter(waterpoint_id=id_field)
    discharge_surveys = filter_discharge_survey(discharge_surveys, paramDict)

    paramDict = request.GET
    discharge_surveys = filter_discharge_survey(discharge_surveys, paramDict)
    for discharge_survey in discharge_surveys:
        discharge_survey.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rds-list', id_field)


@login_required
def export_discharge_survey(request, id_field):
    discharge_surveyresource = discharge_surveyResource()
    paramDict = request.GET
    discharge_surveys = discharge_survey.objects.filter(waterpoint_id=id_field)
    discharge_surveys = filter_discharge_survey(discharge_surveys, paramDict)
    dataset = discharge_surveyresource.export(discharge_surveys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="discharge_surveyresource.xls"'
    return response

@login_required
def river_rds_up_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    discharge_surveys_new = xy_river.discharge_surveys.filter(created_by=request.user)

    paramDict = request.GET
    discharge_surveys_new = filter_discharge_survey(discharge_surveys_new, paramDict)

    x = list()
    for entry in discharge_surveys_new:
        x.append(entry.data_limit_up)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x=len(x)
    today = timezone.now()

    params = {
        'today': today,
        'discharge_surveys_new': discharge_surveys_new,
        'xy_river_inf':xy_river_inf,
        'mean_x': mean_x,

        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,
'count_x':count_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rds_up_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
def river_rds_low_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    discharge_surveys_new = xy_river.discharge_surveys.filter(created_by=request.user)

    paramDict = request.GET
    discharge_surveys_new = filter_discharge_survey(discharge_surveys_new, paramDict)

    x = list()
    for entry in discharge_surveys_new:
        x.append(entry.data_limit_low)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x=len(x)
    today = timezone.now()

    params = {
        'today': today,
        'discharge_surveys_new': discharge_surveys_new,
        'xy_river_inf':xy_river_inf,
        'mean_x': mean_x,

        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,
'count_x':count_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rds_low_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

###################### sectionareasurvey ##############
@login_required
def river_rss_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))

    sectionareasurveys = xy_river.sectionareasurveys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    sectionareasurveys_new = filter_sectionareasurvey(sectionareasurveys, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'sectionareasurveys_new': sectionareasurveys_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date,
        'xy_river': xy_river,
    }
    return render(request, 'observe/river/river_rss_list.html', context)

@login_required
def river_rss_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = sectionareasurveyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the added done successfully!')
            return redirect('rss-list', id_field)
        else:
            messages.warning(request, ' sorry the added failed!')
            return redirect('rss-list', id_field)

    elif (request.method == "GET"):
        form = sectionareasurveyForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rss_form.html', context)


@login_required
@user_is_sectionareasurvey_author
def river_rss_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        sectionareasurveynew = sectionareasurvey.objects.filter(pk=id).first()
        form = sectionareasurveyForm(instance=sectionareasurveynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rss_form.html', context)
    elif request.method == "POST":

        sectionareasurveynew = sectionareasurvey.objects.filter(pk=id).first()
        form = sectionareasurveyForm(request.POST, instance=sectionareasurveynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('rss-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('rss-list', id_field)


@user_is_sectionareasurvey_author
def river_rss_delete(request, id_field, id):
    deleted_sectionareasurvey = sectionareasurvey.objects.get(pk=id)
    deleted_sectionareasurvey.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rss-list', id_field)
@login_required
@user_is_sectionareasurvey_author
def river_sectionareasurvey_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    sectionareasurveys = xy_river.sectionareasurveys.filter(waterpoint_id=id_field)
    sectionareasurveys = filter_sectionareasurvey(sectionareasurveys, paramDict)

    paramDict = request.GET
    sectionareasurveys = filter_sectionareasurvey(sectionareasurveys, paramDict)
    for sectionareasurvey in sectionareasurveys:
        sectionareasurvey.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rss-list', id_field)


@login_required
def export_sectionareasurvey(request, id_field):
    sectionareasurvey_resource = sectionareasurveyResource()
    paramDict = request.GET
    sectionareasurveys = sectionareasurvey.objects.filter(waterpoint_id=id_field)
    sectionareasurveys = filter_sectionareasurvey(sectionareasurveys, paramDict)
    dataset = sectionareasurvey_resource.export(sectionareasurveys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sectionareasurvey.xls"'
    return response

@login_required
def river_rss_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    xy_river_inf = xy_river.river_inf
    id_field = xy_river.id_field
    sectionareasurveys = xy_river.sectionareasurveys.filter(created_by=request.user)

    paramDict = request.GET
    sectionareasurveys_new = filter_sectionareasurvey(sectionareasurveys, paramDict)

    x = list()
    for entry in sectionareasurveys_new:
        x.append(entry.sas_area)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'count_x':count_x,
        'xy_river_inf':xy_river_inf,
        'sectionareasurveys_new': sectionareasurveys_new,
        'mean_x': mean_x,
        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,
        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
    }
    pdf = render_to_pdf('observe/river/rss_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


##########sectiondata ########
@login_required
def river_rsd_list(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    riverinfnew = River_inf.objects.filter(xy_river=xy_river.pk).first()

    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))

    sectiondatas = xy_river.sectiondatas.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    sectiondatas_new = filter_date(sectiondatas, paramDict)
    context = {
        'riverinfnew': riverinfnew,
        'sectiondatas_new': sectiondatas_new,
        'id_field': id_field,
        'map_xy_river': map_xy_river,
        'form_date': form_date
    }
    return render(request, 'observe/river/river_rsd_list.html', context)

@login_required
def river_rsd_create_form(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if (request.method == "POST"):
        form = sectiondataForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_river
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the added done successfully!')
            return redirect('rsd-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('rsd-list', id_field)


    elif (request.method == "GET"):
        form = sectiondataForm()

    context = {
        'form': form,
        'id_field': id_field}

    return render(request, 'observe/river/rsd_form.html', context)


@login_required
@user_is_sectiondata_author
def river_rsd_update_form(request, id_field, id):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    if request.method == "GET":
        sectiondatanew = sectiondata.objects.filter(pk=id).first()
        form = sectiondataForm(instance=sectiondatanew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/river/rsd_form.html', context)
    elif request.method == "POST":

        sectionareasurveynew = sectiondata.objects.filter(pk=id).first()
        form = sectiondataForm(request.POST, instance=sectionareasurveynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('rsd-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('rsd-list', id_field)

@user_is_sectiondata_author
def river_rsd_delete(request, id_field, id):
    deleted_sectiondata = sectiondata.objects.get(pk=id)
    deleted_sectiondata.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rsd-list', id_field)
@login_required
@user_is_sectiondata_author
def river_sectiondata_multi_delete(request,id_field):
    paramDict = request.GET
    xy_river = get_object_or_404(XY_River, pk=id_field)
    sectiondatas = xy_river.sectiondatas.filter(waterpoint_id=id_field)
    sectiondatas = filter_sectiondata(sectiondatas, paramDict)

    paramDict = request.GET
    sectiondatas = filter_sectiondata(sectiondatas, paramDict)
    for sectiondata in sectiondatas:
        sectiondata.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('rsd-list', id_field)


@login_required
def export_sectiondata(request, xy_metology_id):
    sectiondata_resource = sectiondataResource()
    paramDict = request.GET
    sectiondatas = sectiondata.objects.filter(waterpoint_id=xy_metology_id)
    sectiondatas = filter_sectiondata(sectiondatas, paramDict)
    dataset = sectiondata_resource.export(sectiondatas)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sectiondatas.xls"'
    return response

@login_required
def river_rsd_Pdf(request, id_field):
    xy_river = get_object_or_404(XY_River, pk=id_field)
    map_xy_river = serialize('geojson', XY_River.objects.filter(pk=id_field))
    id_field = xy_river.id_field
    sectiondatas_new = xy_river.sectiondatas.filter(created_by=request.user)

    paramDict = request.GET
    sectiondatas_new = filter_sectiondata(sectiondatas_new, paramDict)

    x = list()
    for entry in sectiondatas_new:
        x.append(entry.sec_x)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'sectiondatas_new': sectiondatas_new,
        'mean_x': mean_x,

        'xy_river': xy_river,
        # 'chart': dump,
        'max_x': max_x,

        'min_x': min_x,
        'median_x': median_x,
        'mode_x': mode_x,
        'mean_x': mean_x,

    }
    pdf = render_to_pdf('observe/river/rsd_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')


#################
@login_required
def export_filtered_rivers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="waterpoints.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
         'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x', 'stm_y'])
    waterpoints = XY_River.objects.all()
    paramDict = request.GET
    waterpoints = filter_waterpoints(waterpoints, paramDict)
    waterpoints = waterpoints.values_list(
        'id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
        'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x', 'stm_y')

    for waterpoint in waterpoints:
        writer.writerow(waterpoint)

    return response


def export_filtered_rivers_xls(request):
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

    rows = XY_River.objects.all().values_list('id_field', 'old_id', 'sitename_a', 'sitename_e', 'type', 'agency',
                                              'mohafaza', 'montika', 'nahia', 'village',
                                              'sub_baisn', 'w84_utm_x', 'w84_utm_y', 'w84_utm_z', 'means_z', 'stm_x',
                                              'stm_y')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def simple_upload(request):
    if request.method == 'POST':
        riverdischarge_daily_resource = River_dis_dailyResource()
        dataset = tablib.Dataset()
        new_riverdischarge_daily = request.FILES['myfile']

        imported_data = dataset.load(new_riverdischarge_daily.read())
        result = riverdischarge_daily_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            riverdischarge_daily_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'observe/import.html')


def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        riverdischarge_daily_resource = River_dis_dailyResource()
        dataset = tablib.Dataset()
        new_riverdischarge_daily = request.FILES['importData']
        if file_format == 'xls':
            imported_data = dataset.load(new_riverdischarge_daily.read().decode('utf-8'), format='xls')
            result = riverdischarge_daily_resource.import_data(dataset, dry_run=True)
        if file_format == 'CSV':
            imported_data = dataset.load(new_riverdischarge_daily.read().decode('utf-8'), format='csv')
            result = riverdischarge_daily_resource.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(new_riverdischarge_daily.read().decode('utf-8'), format='json')
            # Testing data import
            result = riverdischarge_daily_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            # Import now
            riverdischarge_daily_resource.import_data(dataset, dry_run=False)

    return render(request, 'observe/import.html')
