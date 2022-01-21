from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.core.serializers import serialize
from observe.wells.decorators import user_is_wells_quality_author,user_is_welltoplevel_author,user_is_auto_groundwater_author,\
user_is_welllogging_author,user_is_lithologging_author,user_is_loggingdata_author,user_is_log_plot_author,user_is_drilling_author,\
user_is_casing_author,user_is_packing_author,user_is_groundwaterlevel_author,user_is_groundwaterlevel_manual_author
from observe.wells.models import XY_Well,groundwaterlevel,wells_quality,welltoplevel,auto_groundwater,welllogging,groundwaterlevel_manual,\
    loggingdata,log_plot,lithologging,drilling,packing,casing,well_inf
from observe.wells.forms import groundwaterlevelForm,groundwaterlevel_manualForm,auto_groundwaterForm,wellloggingForm,wells_qualityForm,welltoplevelForm,\
    lithologgingForm,log_plotForm,drillingForm,casingForm,packingForm,loggingdataForm,Well_infForm
from observe.wells.filter import filter_drilling,filter_casing,filter_packing,filter_lithologging,filter_welllogging,\
    filter_auto_groundwater,filter_welltoplevel,filter_wells_quality,filter_groundwaterlevel_manual,filter_groundwaterlevel
from observe.wells.resources import wellloggingResource,wells_qualityResource,auto_groundwaterResource,groundwaterlevel_manualResource,\
    groundwaterlevelResource,welltoplevelResource,drillingResource,casingResource,packingResource,lithologgingResource,log_plotResource,loggingdataResource
import statistics
import scipy.stats
from django.utils import timezone
from observe.utils.utils import render_to_pdf
from observe.forms import QueryForm ,QueryDateForm
from observe.utils.filter import filter_date
from observe.utils.filter import filter_waterpoints
import csv
import xlwt

def all_xy_wells(request):
  XY_Wells = XY_Well.objects.all()
  form = QueryForm(request.GET or None)
  paramDict = request.GET
  XY_Wells = filter_waterpoints(XY_Wells, paramDict)
  map_XY_Wells = serialize('geojson', XY_Wells)

  # print(map_waterpoints)
  context = {
        'XY_Wells': XY_Wells,
        'map_XY_Wells':map_XY_Wells,
        'form': form,
    }
  return render(request, 'observe/wells.html', context)



def import_well_readings(request):
    XY_Wells = XY_Well.objects.all()

    map_XY_Wells= serialize('geojson', XY_Wells)


    context = {
        'XY_Wells': XY_Wells,
        'map_XY_Wells': map_XY_Wells,

    }
    return render(request,'observe/well_import_form.html',context)

###############
from observe.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from django.urls import reverse
from observe.wells.forms import WellForm
from observe.wells.models import XY_Well
from django.contrib import messages

################# add edit delete metology point
class WellListView( BaseListView):
    model = XY_Well
    paginate_by = 100  # if pagination is desired
class WellCreate( BaseCreateView):
    model = XY_Well
    form_class = WellForm

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        created_by = self.request.user
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'Your point was  saved successfully!')
        return super().form_valid(form)
class WellUpdate( BaseUpdateView):
    model = XY_Well
    form_class = WellForm
    template_name = 'observe/well_form.html'
    def form_valid(self, form):
        image = self.request.FILES.get('image')
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Your point was  updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        xy_well = self.get_object()
        if self.request.user == xy_well.created_by:
            return True
        else:
            return False
class WellDelete( BaseDeleteView):
    model = XY_Well
    def get_success_url(self):
        return reverse('xy_wells')


################ Well_inf
def well_inf_update_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    if request.method=="GET":
        form = Well_infForm(instance=wellinfnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/wellinf_form.html', context)
    elif request.method=="POST":
        form = Well_infForm(request.POST,instance=wellinfnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully!')
            return redirect('xy_wells')
##################### start groundwaterlevels#############

def well_gwl_list(request,id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    print(map_xy_well)
    print(3)
    ##############groundwaterlevels#############
    groundwaterlevels = xy_well.groundwaterlevels.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET

    groundwaterlevels_new = filter_groundwaterlevel(groundwaterlevels, paramDict)
    context={
        'wellinfnew':wellinfnew,
        'groundwaterlevels_new':groundwaterlevels_new,
        'id_field':id_field,
        'map_xy_well':map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well,
    }
    return render(request,'observe/well/well_gwl_list.html',context)
def well_gwl_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = groundwaterlevelForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('gwl-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('gwl-list', id_field)

    elif (request.method=="GET") :
        form = groundwaterlevelForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/gwl_form.html',context)

@user_is_groundwaterlevel_author
def well_gwl_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        groundwaterlevelnew = groundwaterlevel.objects.filter(pk=id).first()
        form = groundwaterlevelForm(instance=groundwaterlevelnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/gwl_form.html', context)
    elif request.method=="POST":

        groundwaterlevelnew = groundwaterlevel.objects.filter(pk=id).first()
        form = groundwaterlevelForm(request.POST,instance=groundwaterlevelnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('gwl-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('gwl-list', id_field)
@login_required()
def well_gwl_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    groundwaterlevels_new = xy_well.groundwaterlevels.filter(created_by=request.user)

    paramDict = request.GET
    groundwaterlevels_new = filter_groundwaterlevel(groundwaterlevels_new, paramDict)

    x = list()
    for entry in groundwaterlevels_new:
     x.append(entry.waterlevel)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'groundwaterlevels_new': groundwaterlevels_new,
        'xy_well_inf':xy_well_inf,
        'count_x':count_x,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/gwl_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required()
def well_gwd_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    groundwaterlevels_new = xy_well.groundwaterlevels.filter(created_by=request.user)

    paramDict = request.GET
    groundwaterlevels_new = filter_groundwaterlevel(groundwaterlevels_new, paramDict)

    x = list()
    for entry in groundwaterlevels_new:
     x.append(entry.depth_to_water)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'groundwaterlevels_new': groundwaterlevels_new,
        'xy_well_inf':xy_well_inf,
        'count_x':count_x,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/gwd_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_groundwaterlevel_author
def well_gwl_delete(request ,id_field,id):
    deleted_groundwaterlevel = groundwaterlevel.objects.get(pk=id)
    deleted_groundwaterlevel.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('gwl-list', id_field)
@user_is_groundwaterlevel_author
def well_gwl_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    groundwaterlevels = xy_well.groundwaterlevels.filter(waterpoint_id=id_field)
    groundwaterlevels = filter_groundwaterlevel(groundwaterlevels, paramDict)

    paramDict = request.GET
    groundwaterlevels = filter_groundwaterlevel(groundwaterlevels, paramDict)
    for groundwaterlevel in groundwaterlevels:
        groundwaterlevel.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('gwl-list', id_field)
@login_required()
def export_well_groundwaterlevels(request,id_field):
    groundwaterlevel_resource = groundwaterlevelResource()
    paramDict = request.GET
    groundwaterlevels = groundwaterlevel.objects.filter(waterpoint_id=id_field)
    groundwaterlevels = filter_groundwaterlevel(groundwaterlevels, paramDict)


    dataset = groundwaterlevel_resource.export(groundwaterlevels)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="groundwaterlevel.xls"'
    return response

#########start auto_groundwater###########
@login_required()
def well_agw_list(request,id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))

    auto_groundwaters = xy_well.auto_groundwaters.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    auto_groundwaters_new = filter_auto_groundwater(auto_groundwaters, paramDict)
    context={
        'wellinfnew':wellinfnew,
        'auto_groundwaters_new':auto_groundwaters_new,
        'id_field':id_field,
        'xy_well':xy_well,
        'map_xy_well':map_xy_well,
        'form_date':form_date
    }
    return render(request,'observe/well/well_agw_list.html',context)
@login_required()
def well_agw_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = auto_groundwaterForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully')
            return redirect('agw-list', id_field)
        else:
            messages.warning(request,'sorry the added failed')
            return redirect('agw-list', id_field)

    elif (request.method=="GET") :
        form = auto_groundwaterForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/agw_form.html',context)

@user_is_auto_groundwater_author
def well_agw_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        auto_groundwaternew = auto_groundwater.objects.filter(pk=id).first()
        form = auto_groundwaterForm(instance=auto_groundwaternew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/agw_form.html', context)
    elif request.method=="POST":

        auto_groundwaternew = auto_groundwater.objects.filter(pk=id).first()
        form = auto_groundwaterForm(request.POST,instance=auto_groundwaternew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully')
            return redirect('agw-list', id_field)
        else:
            messages.warning(request,'sorry the updated failed!')
            return redirect('agw-list', id_field)
@login_required()
def well_agw_level_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    auto_groundwaters_new = xy_well.auto_groundwaters.filter(created_by=request.user)

    paramDict = request.GET
    auto_groundwaters_new = filter_auto_groundwater(auto_groundwaters_new, paramDict)

    x = list()
    for entry in auto_groundwaters_new:
     x.append(entry.gw_level_m)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'auto_groundwaters_new': auto_groundwaters_new,
        'xy_well_inf':xy_well_inf,
        'count_x':count_x,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/agw_level_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required()
def well_agw_depth_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    auto_groundwaters_new = xy_well.auto_groundwaters.filter(created_by=request.user)

    paramDict = request.GET
    auto_groundwaters_new = filter_auto_groundwater(auto_groundwaters_new, paramDict)

    x = list()
    for entry in auto_groundwaters_new:
     x.append(entry.depth_m)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'auto_groundwaters_new': auto_groundwaters_new,
        'xy_well_inf':xy_well_inf,
        'count_x':count_x,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/agw_depth_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@user_is_auto_groundwater_author
def well_agw_delete(request ,id_field,id):
    deleted_auto_groundwater = auto_groundwater.objects.get(pk=id)
    deleted_auto_groundwater.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('agw-list', id_field)
@user_is_auto_groundwater_author
def well_agw_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    auto_groundwaters = xy_well.auto_groundwaters.filter(waterpoint_id=id_field)
    auto_groundwaters = filter_auto_groundwater(auto_groundwaters, paramDict)

    paramDict = request.GET
    auto_groundwaters = filter_auto_groundwater(auto_groundwaters, paramDict)
    for auto_groundwater in auto_groundwaters:
        auto_groundwater.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('agw-list', id_field)
@login_required()
def export_well_auto_groundwater(request,id_field):
    auto_groundwater_resource = auto_groundwaterResource()
    paramDict = request.GET
    auto_groundwaters = auto_groundwater.objects.filter(waterpoint_id=id_field)
    auto_groundwaters = filter_auto_groundwater(auto_groundwaters, paramDict)


    dataset = auto_groundwater_resource.export(auto_groundwaters)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="auto_groundwater.xls"'
    return response

# ######################start groundwaterlevel_manuals #########
@login_required()
def well_gwlm_list(request,id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    ##############groundwaterlevel manuals#############
    groundwaterlevel_manuals = xy_well.groundwaterlevel_manuals.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET

    groundwaterlevel_manuals_new = filter_groundwaterlevel_manual(groundwaterlevel_manuals, paramDict)
    context={
        'wellinfnew':wellinfnew,
        'groundwaterlevel_manuals_new':groundwaterlevel_manuals_new,
        'id_field':id_field,
        'map_xy_well':map_xy_well,
        'form_date':form_date
    }
    return render(request,'observe/well/well_gwlm_list.html',context)
@login_required()
def well_gwlm_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = groundwaterlevel_manualForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('gwlm-list', id_field)
        else:
            messages.warning(request, ' sorry the  added failed!')
            return redirect('gwlm-list', id_field)

    elif (request.method=="GET") :
        form = groundwaterlevel_manualForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/gwlm_form.html',context)

@user_is_groundwaterlevel_manual_author
def well_gwlm_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        groundwaterlevel_manualnew = groundwaterlevel_manual.objects.filter(pk=id).first()
        form = groundwaterlevel_manualForm(instance=groundwaterlevel_manualnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/gwlm_form.html', context)
    elif request.method=="POST":

        groundwaterlevel_manualnew = groundwaterlevel_manual.objects.filter(pk=id).first()
        form = groundwaterlevel_manualForm(request.POST,instance=groundwaterlevel_manualnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('gwlm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('gwlm-list', id_field)
@login_required()
def well_gwlm_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    id_field =xy_well.id_field
    groundwaterlevel_manuals = xy_well.groundwaterlevel_manuals.filter(created_by=request.user)

    paramDict = request.GET
    groundwaterlevel_manuals_new = filter_groundwaterlevel_manual(groundwaterlevel_manuals, paramDict)

    x = list()
    for entry in groundwaterlevel_manuals_new:
     x.append(entry.depth_to_water)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'groundwaterlevel_manuals_new': groundwaterlevel_manuals_new,
         'mean_x':mean_x,
         'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
    }
    pdf = render_to_pdf('observe/well/gwlm_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_groundwaterlevel_manual_author
def well_gwlm_delete(request ,id_field,id):
    deleted_groundwaterlevel_manual = groundwaterlevel_manual.objects.get(pk=id)
    deleted_groundwaterlevel_manual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('gwlm-list', id_field)

@user_is_groundwaterlevel_manual_author
def well_gwlm_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    groundwaterlevel_manuals = xy_well.groundwaterlevel_manuals.filter(waterpoint_id=id_field)
    groundwaterlevel_manuals = filter_groundwaterlevel_manual(groundwaterlevel_manuals, paramDict)

    paramDict = request.GET
    groundwaterlevel_manuals = filter_groundwaterlevel_manual(groundwaterlevel_manuals, paramDict)
    for groundwaterlevel_manual in groundwaterlevel_manuals:
        groundwaterlevel_manual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('gwlm-list', id_field)
@login_required()
def export_well_groundwaterlevel_manuals(request,id_field):
    groundwaterlevel_manual_resource = groundwaterlevel_manualResource()
    paramDict = request.GET
    groundwaterlevel_manuals = groundwaterlevel_manual.objects.filter(waterpoint_id=id_field)
    groundwaterlevel_manuals = filter_groundwaterlevel_manual(groundwaterlevel_manuals, paramDict)


    dataset = groundwaterlevel_manual_resource.export(groundwaterlevel_manuals)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="groundwaterlevel_manuals.xls"'
    return response


# ######################well Quality # ######
@login_required()
def well_wq_list(request,id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    wells_qualitys = xy_well.wells_qualitys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    wells_qualitys_new = filter_wells_quality(wells_qualitys, paramDict)
    context={
        'wellinfnew':wellinfnew,
        'wells_qualitys_new':wells_qualitys_new,
        'id_field':id_field,
        'map_xy_well':map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well,

    }
    return render(request,'observe/well/well_wq_list.html',context)
@login_required()
def well_wq_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = wells_qualityForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('wq-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('wq-list', id_field)

    elif (request.method=="GET") :
        form = wells_qualityForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/wq_form.html',context)

@user_is_wells_quality_author
def well_wq_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        wells_qualitynew = wells_quality.objects.filter(pk=id).first()
        form = wells_qualityForm(instance=wells_qualitynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/wq_form.html', context)
    elif request.method=="POST":

        wells_qualitynew = wells_quality.objects.filter(pk=id).first()
        form = wells_qualityForm(request.POST,instance=wells_qualitynew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully!')
            return redirect('wq-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('wq-list', id_field)
@login_required()
def well_wq_ph_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    wells_qualitys_new = xy_well.wells_qualitys.filter(created_by=request.user)

    paramDict = request.GET
    wells_qualitys_new = filter_wells_quality(wells_qualitys_new, paramDict)

    x = list()
    for entry in wells_qualitys_new:
     x.append(entry.ph)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x =len(x)
    today = timezone.now()

    params = {
        'today': today,
        'wells_qualitys_new': wells_qualitys_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_well_inf':xy_well_inf,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
    }
    pdf = render_to_pdf('observe/well/wq_ph_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required()
def well_wq_ec_ms_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    wells_qualitys_new = xy_well.wells_qualitys.filter(created_by=request.user)

    paramDict = request.GET
    wells_qualitys_new = filter_wells_quality(wells_qualitys_new, paramDict)

    x = list()
    for entry in wells_qualitys_new:
     x.append(entry.ec_ms_m)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x =len(x)
    today = timezone.now()

    params = {
        'today': today,
        'wells_qualitys_new': wells_qualitys_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_well_inf':xy_well_inf,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
    }
    pdf = render_to_pdf('observe/well/wq_ec_ms_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@user_is_wells_quality_author
def well_wq_delete(request ,id_field,id):
    deleted_wells_quality = wells_quality.objects.get(pk=id)
    deleted_wells_quality.delete()
    messages.success(request, 'the updated done successfully!')
    return redirect('wq-list', id_field)
@user_is_wells_quality_author
def well_wq_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wells_qualitys = xy_well.wells_qualitys.filter(waterpoint_id=id_field)
    wells_qualitys = filter_wells_quality(wells_qualitys, paramDict)

    paramDict = request.GET
    wells_qualitys = filter_wells_quality(wells_qualitys, paramDict)
    for wells_quality in wells_qualitys:
        wells_quality.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('wq-list', id_field)
@login_required()
def export_wells_quality(request,id_field):
    wells_quality_resource = wells_qualityResource()
    paramDict = request.GET
    wells_qualitys = wells_quality.objects.filter(waterpoint_id=id_field)
    wells_qualitys = filter_groundwaterlevel_manual(wells_qualitys, paramDict)


    dataset = wells_quality_resource.export(wells_qualitys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="wells_quality.xls"'
    return response

#  #########################welltoplevels########
@login_required()
def well_wtl_list(request,id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))

    welltoplevels = xy_well.welltoplevels.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    welltoplevels_new = filter_welltoplevel(welltoplevels, paramDict)
    context={
        'wellinfnew':wellinfnew,
        'welltoplevels_new':welltoplevels_new,
        'id_field':id_field,
        'map_xy_well':map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well,
    }
    return render(request,'observe/well/well_wtl_list.html',context)
@login_required()
def well_wtl_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = welltoplevelForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('wtl-list', id_field)
        else:
            messages.success(request, 'sorry the  added failed!')
            return redirect('wtl-list', id_field)

    elif (request.method=="GET") :
        form = welltoplevelForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/wtl_form.html',context)

@user_is_welltoplevel_author
def well_wtl_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        welltoplevelnew = welltoplevel.objects.filter(pk=id).first()
        form = welltoplevelForm(instance=welltoplevelnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/wtl_form.html', context)
    elif request.method=="POST":

        welltoplevelnew = welltoplevel.objects.filter(pk=id).first()
        form = welltoplevelForm(request.POST,instance=welltoplevelnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully!')
            return redirect('wtl-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('wtl-list', id_field)
@login_required()
def well_wtl_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    xy_well_inf = xy_well.well_inf
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    id_field =xy_well.id_field
    welltoplevels_new = xy_well.welltoplevels.filter(created_by=request.user)

    paramDict = request.GET
    welltoplevels_new = filter_welltoplevel(welltoplevels_new, paramDict)

    x = list()
    for entry in welltoplevels_new:
     x.append(entry.ground_level)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()
    params = {
        'today': today,
        'welltoplevels_new': welltoplevels_new,
         'mean_x':mean_x,
        'xy_well_inf':xy_well_inf,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'count_x':count_x,
        'mode_x':mode_x,
    }
    pdf = render_to_pdf('observe/well/wtl_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_welltoplevel_author
def well_wtl_delete(request ,id_field,id):
    deleted_welltoplevel = welltoplevel.objects.get(pk=id)
    deleted_welltoplevel.delete()
    messages.success(request, 'the updated done successfully!')
    return redirect('wtl-list', id_field)
@user_is_welltoplevel_author
def well_wtl_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    welltoplevels = xy_well.welltoplevels.filter(waterpoint_id=id_field)
    welltoplevels = filter_welltoplevel(welltoplevels, paramDict)

    paramDict = request.GET
    welltoplevels = filter_welltoplevel(welltoplevels, paramDict)
    for welltoplevel in welltoplevels:
        welltoplevel.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('wtl-list', id_field)
@login_required()
def export_welltoplevel(request,id_field):
    welltoplevels_resource = welltoplevelResource()
    paramDict = request.GET
    welltoplevels = welltoplevel.objects.filter(waterpoint_id=id_field)
    welltoplevels = filter_welltoplevel(welltoplevels, paramDict)


    dataset = welltoplevels_resource.export(welltoplevels)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="welltoplevels.xls"'
    return response


#  ###############wellloggings##########
@login_required()
def well_wl_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    wellloggings = xy_well.wellloggings.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    wellloggings_new = filter_welllogging(wellloggings, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'wellloggings_new': wellloggings_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well,
    }
    return render(request, 'observe/well/well_wl_list.html', context)
@login_required()
def well_wl_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = wellloggingForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('wl-list', id_field)
        else:
            messages.warning(request, 'sorry the  added failed!')
            return redirect('wl-list', id_field)

    elif (request.method=="GET") :
        form = wellloggingForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/wl_form.html',context)

@user_is_welllogging_author
def well_wl_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        wellloggingnew = welllogging.objects.filter(pk=id).first()
        form = wellloggingForm(instance=wellloggingnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/wl_form.html', context)
    elif request.method=="POST":

        wellloggingnew = welllogging.objects.filter(pk=id).first()
        form = wellloggingForm(request.POST,instance=wellloggingnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully')
            return redirect('wl-list', id_field)
        else:
            messages.warning(request,'sorry the updated failed')
            return redirect('wl-list', id_field)

@user_is_welllogging_author
def well_wl_delete(request, id_field, id):
    deleted_welllogging = welllogging.objects.get(pk=id)
    deleted_welllogging.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('wl-list', id_field)
@user_is_welllogging_author
def well_wl_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellloggings = xy_well.wellloggings.filter(waterpoint_id=id_field)
    wellloggings = filter_welllogging(wellloggings, paramDict)

    paramDict = request.GET
    wellloggings = filter_welllogging(wellloggings, paramDict)
    for welllogging in wellloggings:
        welllogging.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('wtl-list', id_field)
@login_required()
def well_log_pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    xy_well_inf = xy_well.well_inf
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    id_field =xy_well.id_field
    wellloggings_new = xy_well.wellloggings.filter(created_by=request.user)

    paramDict = request.GET
    wellloggings_new = filter_welllogging(wellloggings_new, paramDict)


    today = timezone.now()
    params = {
        'today': today,
        'wellloggings_new': wellloggings_new,

        'xy_well_inf':xy_well_inf,
        'xy_well':xy_well,

    }
    pdf = render_to_pdf('observe/well/wl_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required()
def export_welllogging(request,id_field):
    welllogging_resource = wellloggingResource()
    paramDict = request.GET
    wellloggings = welllogging.objects.filter(waterpoint_id=id_field)
    wellloggings = filter_welllogging(wellloggings, paramDict)


    dataset = welllogging_resource.export(wellloggings)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="wellloggings.xls"'
    return response

########################## lithologging ######
@login_required()
def well_ll_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    lithologgings = xy_well.lithologgings.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    lithologgings_new = filter_lithologging(lithologgings, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'lithologgings_new': lithologgings_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well,
    }
    return render(request, 'observe/well/well_ll_list.html', context)
@login_required()
def well_ll_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = lithologgingForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('ll-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed!')
            return redirect('ll-list', id_field)

    elif (request.method=="GET") :
        form = lithologgingForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/ll_form.html',context)
@user_is_lithologging_author
def well_ll_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        lithologgingnew = lithologging.objects.filter(pk=id).first()
        form = lithologgingForm(instance=lithologgingnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/ll_form.html', context)
    elif request.method=="POST":

        lithologgingnew = lithologging.objects.filter(pk=id).first()
        form = lithologgingForm(request.POST,instance=lithologgingnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully')
            return redirect('ll-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('ll-list', id_field)
@login_required()
def well_ll_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    lithologgings_new = xy_well.lithologgings.filter(created_by=request.user)

    paramDict = request.GET
    lithologgings_new = filter_lithologging(lithologgings_new, paramDict)

    x = list()
    for entry in lithologgings_new:
     x.append(entry.sgwl)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x =len(x)
    today = timezone.now()

    params = {
        'today': today,
        'lithologgings_new': lithologgings_new,
        'xy_well_inf':xy_well_inf,
        'count_x':count_x,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
    }
    pdf = render_to_pdf('observe/well/ll_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@user_is_lithologging_author
def well_ll_delete(request, id_field, id):
    deleted_lithologging = lithologging.objects.get(pk=id)
    deleted_lithologging.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('ll-list', id_field)
@user_is_lithologging_author
def well_ll_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    lithologgings = xy_well.lithologgings.filter(waterpoint_id=id_field)
    lithologgings = filter_lithologging(lithologgings, paramDict)

    paramDict = request.GET
    lithologgings = filter_lithologging(lithologgings, paramDict)
    for lithologging in lithologgings:
        lithologging.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('ll-list', id_field)
@login_required()
def export_lithologging(request,id_field):
    lithologging_resource = lithologgingResource()
    paramDict = request.GET
    lithologgings = lithologging.objects.filter(waterpoint_id=id_field)
    lithologgings = filter_lithologging(lithologgings, paramDict)


    dataset = lithologging_resource.export(lithologgings)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="lithologging.xls"'
    return response

########################## loggingdata without export  ######
@login_required()
def well_ld_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    loggingdatas = xy_well.loggingdatas.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    loggingdatas_new = filter_date(loggingdatas, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'loggingdatas_new': loggingdatas_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
    }
    return render(request, 'observe/well/well_ld_list.html', context)
@login_required()
def well_ld_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = loggingdataForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('ld-list', id_field)
        else:
            messages.warning(request, 'sorry the  added failed!')
            return redirect('ld-list', id_field)

    elif (request.method=="GET") :
        form = loggingdataForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/wl_form.html',context)
@user_is_loggingdata_author
def well_ld_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        loggingdatanew = loggingdata.objects.filter(pk=id).first()
        form = loggingdataForm(instance=loggingdatanew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/wl_form.html', context)
    elif request.method=="POST":

        loggingdatanew = loggingdata.objects.filter(pk=id).first()
        form = loggingdataForm(request.POST,instance=loggingdatanew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully!')
            return redirect('ld-list', id_field)
        else:
            messages.warning(request,'sorry the updated failed!')
            return redirect('ld-list', id_field)
# def well_ld_Pdf(request,id_field):
#
#     xy_well = get_object_or_404(XY_Well, pk=id_field)
#     map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
#     id_field =xy_well.id_field
#     loggingdatas_new = xy_well.loggingdatas.filter(created_by=request.user)
#
#     paramDict = request.GET
#     loggingdatas_new = filter_loggingdata(loggingdatas_new, paramDict)
#
#     x = list()
#     for entry in loggingdatas_new:
#      x.append(entry.depth)
#     mean_x = statistics.mean(x)
#     median_x = statistics.median(x)
#     mode_x = statistics.multimode(x)
#     max_x = max(x)
#     min_x = min(x)
#     today = timezone.now()
#
#     params = {
#         'today': today,
#         'loggingdatas_new': loggingdatas_new,
#          'mean_x':mean_x,
#         'xy_well':xy_well,
#         'max_x':max_x,
#         'min_x':min_x,
#         'median_x':median_x,
#         'mode_x':mode_x,
#         'mean_x':mean_x,
#     }
#     pdf = render_to_pdf('observe/well/ld_report.html', params)
#     return HttpResponse(pdf, content_type='application/pdf')
@user_is_loggingdata_author
def well_ld_delete(request, id_field, id):
    deleted_loggingdata = loggingdata.objects.get(pk=id)
    deleted_loggingdata.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('ld-list', id_field)

# def well_ld_multi_delete(request,id_field):
#     paramDict = request.GET
#     xy_well = get_object_or_404(XY_Well, pk=id_field)
#     loggingdatas = xy_well.loggingdatas.filter(waterpoint_id=id_field)
#     loggingdatas = filter_loggingdata(loggingdatas, paramDict)
#
#     paramDict = request.GET
#     loggingdatas = filter_loggingdata(loggingdatas, paramDict)
#     for loggingdata in loggingdatas:
#         loggingdata.delete()
#     messages.success(request, 'the deleted done successfully!')
#     return redirect('ld-list', id_field)


########################## logg_plot without export ######
@login_required()
def well_lp_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    log_plots = xy_well.log_plots.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    log_plots_new = filter_date(log_plots, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'log_plots_new': log_plots_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
        'xy_well':xy_well
    }
    return render(request, 'observe/well/well_lp_list.html', context)
@login_required()
def well_lp_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = log_plotForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('lp-list', id_field)
        else:
            messages.success(request, 'sorry the added failed!')
            return redirect('lp-list', id_field)

    elif (request.method=="GET") :
        form = log_plotForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/lp_form.html',context)
@user_is_log_plot_author
def well_lp_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        log_plotnew = log_plot.objects.filter(pk=id).first()
        form = log_plotForm(instance=log_plotnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/lp_form.html', context)
    elif request.method=="POST":

        log_plotnew = log_plot.objects.filter(pk=id).first()
        form = log_plotForm(request.POST,instance=log_plotnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully')
            return redirect('lp-list', id_field)
        else:
            messages.warning(request, ' sorry the updated failed')
            return redirect('lp-list', id_field)

@user_is_log_plot_author
def well_lp_delete(request, id_field, id):
    deleted_log_plot = log_plot.objects.get(pk=id)
    deleted_log_plot.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('lp-list', id_field)


########################## drilling######
@login_required()
def well_drill_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    drillings = xy_well.drillings.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    drillings_new = filter_drilling(drillings, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'drillings_new': drillings_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well
    }
    return render(request, 'observe/well/well_drill_list.html', context)
@login_required()
def well_drill_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = drillingForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully')
            return redirect('drill-list', id_field)
        else:
            messages.warning(request, 'sorry the  added failed')
            return redirect('drill-list', id_field)

    elif (request.method=="GET") :
        form = drillingForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/drill_form.html',context)
@user_is_drilling_author
def well_drill_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        drillingnew = drilling.objects.filter(pk=id).first()
        form = drillingForm(instance=drillingnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/drill_form.html', context)
    elif request.method=="POST":

        drillingnew = drilling.objects.filter(pk=id).first()
        form = drillingForm(request.POST,instance=drillingnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully')
            return redirect('drill-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('drill-list', id_field)
@login_required()
def well_drill_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf =xy_well.well_inf
    id_field =xy_well.id_field
    drillings_new = xy_well.drillings.filter(created_by=request.user)

    paramDict = request.GET
    drillings_new = filter_drilling(drillings_new, paramDict)

    x = list()
    for entry in drillings_new:
     x.append(entry.drilling_diameter)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'drillings_new': drillings_new,
        'xy_well_inf':xy_well_inf,
        'count_x':count_x,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/drill_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@user_is_drilling_author
def well_drill_delete(request, id_field, id):
    deleted_drilling = drilling.objects.get(pk=id)
    deleted_drilling.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('drill-list', id_field)
@user_is_drilling_author
def well_drill_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    drillings = xy_well.drillings.filter(waterpoint_id=id_field)
    drillings = filter_drilling(drillings, paramDict)

    paramDict = request.GET
    drillings = filter_drilling(drillings, paramDict)
    for drilling in drillings:
        drilling.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('ld-list', id_field)
@login_required()
def export_drilling(request,id_field):
    drilling_resource = drillingResource()
    paramDict = request.GET
    drillings = drilling.objects.filter(waterpoint_id=id_field)
    drillings = filter_lithologging(drillings, paramDict)


    dataset = drilling_resource.export(drillings)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="drilling.xls"'
    return response

########################## casing######
@login_required()
def well_casing_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    casings = xy_well.casings.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    casings_new = filter_casing(casings, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'xy_well':xy_well,
        'casings_new': casings_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
        'form_date':form_date,
    }
    return render(request, 'observe/well/well_casing_list.html', context)
@login_required()
def well_casing_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = casingForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully')
            return redirect('casing-list', id_field)
        else:
            messages.warning(request, 'sorry the added failed')
            return redirect('casing-list', id_field)

    elif (request.method=="GET") :
        form = casingForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/casing_form.html',context)
@user_is_casing_author
def well_casing_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        casingnew = casing.objects.filter(pk=id).first()
        form = casingForm(instance=casingnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/casing_form.html', context)
    elif request.method=="POST":

        casingnew = casing.objects.filter(pk=id).first()
        form = casingForm(request.POST,instance=casingnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully')
            return redirect('casing-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed')
            return redirect('casing-list', id_field)
@login_required()
def well_casing_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    xy_well_inf = xy_well.well_inf
    id_field =xy_well.id_field
    casings_new = xy_well.casings.filter(created_by=request.user)

    paramDict = request.GET
    casings_new = filter_casing(casings_new, paramDict)

    x = list()
    for entry in casings_new:
     x.append(entry.casing_diameter)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'casings_new': casings_new,
        'count_x':count_x,
        'xy_well_inf':xy_well_inf,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/casing_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@user_is_casing_author
def well_casing_delete(request, id_field, id):
    deleted_casing = casing.objects.get(pk=id)
    deleted_casing.delete()
    messages.success(request, 'the deleted done successfully')
    return redirect('casing-list', id_field)
@user_is_casing_author
def well_casing_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    casings = xy_well.casings.filter(waterpoint_id=id_field)
    casings = filter_casing(casings, paramDict)

    paramDict = request.GET
    casings = filter_casing(casings, paramDict)
    for casing in casings:
        casing.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('ld-list', id_field)

def export_casing(request,id_field):
    casing_resource = casingResource()
    paramDict = request.GET
    casings = casing.objects.filter(waterpoint_id=id_field)
    casings = filter_casing(casings, paramDict)


    dataset = casing_resource.export(casings)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="casing.xls"'
    return response


########################## packing######
@login_required()
def well_packing_list(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    wellinfnew = well_inf.objects.filter(xy_well= xy_well.pk).first()

    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    packings = xy_well.packings.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    packings_new = filter_packing(packings, paramDict)
    context = {
        'wellinfnew':wellinfnew,
        'packings_new': packings_new,
        'id_field': id_field,
        'map_xy_well': map_xy_well,
        'form_date':form_date,
        'xy_well':xy_well,
    }
    return render(request, 'observe/well/well_packing_list.html', context)
@login_required()
def well_packing_create_form(request, id_field):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if (request.method=="POST") :
        form = packingForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_well
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully!')
            return redirect('packing-list', id_field)
        else:
            messages.success(request, 'sorry the added failed!')
            return redirect('packing-list', id_field)

    elif (request.method=="GET") :
        form = packingForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/well/packing_form.html',context)
@user_is_packing_author
def well_packing_update_form(request, id_field ,id):
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    if request.method=="GET":
        casingnew = packing.objects.filter(pk=id).first()
        form = packingForm(instance=casingnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/well/packing_form.html', context)
    elif request.method=="POST":

        packingnew = packing.objects.filter(pk=id).first()
        form = packingForm(request.POST,instance=packingnew)
        if form.is_valid():
            form.save()
            messages.success(request,'the updated done successfully!')
            return redirect('packing-list', id_field)
        else:
            messages.warning(request, 'sorry the updated failed!')
            return redirect('packing-list', id_field)
@login_required()
def well_packing_Pdf(request,id_field):

    xy_well = get_object_or_404(XY_Well, pk=id_field)
    map_xy_well = serialize('geojson', XY_Well.objects.filter(pk=id_field))
    id_field =xy_well.id_field
    packings_new = xy_well.packings.filter(created_by=request.user)

    paramDict = request.GET
    packings_new = filter_packing(packings_new, paramDict)

    x = list()
    for entry in packings_new:
     x.append(entry.packing_diameter)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    today = timezone.now()

    params = {
        'today': today,
        'packings_new': packings_new,
         'mean_x':mean_x,
        'xy_well':xy_well,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/well/drill_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_packing_author
def well_packing_delete(request, id_field, id):
    deleted_packing = packing.objects.get(pk=id)
    deleted_packing.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('packing-list', id_field)
    return redirect('packing-list', id_field)
@user_is_packing_author
def well_packing_multi_delete(request,id_field):
    paramDict = request.GET
    xy_well = get_object_or_404(XY_Well, pk=id_field)
    packings = xy_well.packings.filter(waterpoint_id=id_field)
    packings = filter_packing(packings, paramDict)

    paramDict = request.GET
    packings = filter_packing(packings, paramDict)
    for packing in packings:
        packing.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('ld-list', id_field)
@login_required()
def export_packing(request,id_field):
    packing_resource = packingResource()
    paramDict = request.GET
    packings = packing.objects.filter(waterpoint_id=id_field)
    packings = filter_casing(packings, paramDict)
    dataset = packing_resource.export(packings)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="packing.xls"'
    return response
@login_required()
def export_filtered_wells_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="waterpoints.csv"'

    writer = csv.writer(response)
    writer.writerow(['id_field',   'old_id',    'sitename_a',   'sitename_e',    'type',   'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y'])
    waterpoints = XY_Well.objects.all()
    paramDict = request.GET
    waterpoints = filter_waterpoints(waterpoints, paramDict)
    waterpoints = waterpoints.values_list(
        'id_field',   'old_id',    'sitename_a',   'sitename_e',    'type',   'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y')

    for waterpoint in waterpoints:
        writer.writerow(waterpoint)

    return response
@login_required()
def export_filtered_wells_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="waterpoints.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('waterpoints')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns =  ['id_field',   'old_id',    'sitename_a',   'sitename_e',    'type',   'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    rows = XY_Well.objects.all().values_list('id_field',   'old_id',    'sitename_a', 'sitename_e', 'type', 'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
