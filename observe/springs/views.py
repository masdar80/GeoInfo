from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render,get_object_or_404,redirect
from django.core.serializers import serialize
from observe.springs.models import Spring_inf , XY_Spring,springdischarge_anual,springdischarge_avg_anual,springdischarge_monthly,springdischarge_avg_monthly,springdischarge_daily
from observe.springs.forms import spring_discharge_dailyForm,springdischarge_anualForm,QueryDateAnnualForm,\
    springdischarge_avg_anualForm,springdischarge_avg_monthlyForm,springdischarge_monthlyForm,Spring_infForm,QueryDateMonthForm
from observe.forms import QueryForm,QueryDateForm
    # ,river_discharge_dailyForm
from observe.springs.resources import springdischarge_anualResource,springdischarge_avg_anualResource,springdischarge_avg_monthlyResource,\
    springdischarge_dailyResource,springdischarge_monthlyResource
from observe.springs.filter import filter_springdischarge_anual,filter_springdischarge_avg_anual,filter_springdischarge_avg_monthly,filter_springdischarge_daily,\
    filter_springdischarge_monthly
from observe.springs.decorators import user_is_springdischarge_anual_author,user_is_springdischarge_avg_anual_author,user_is_springdischarge_monthly_author,\
user_is_springdischarge_avg_monthly_author,user_is_springdischarge_daily_author
from observe.utils.filter import filter_waterpoints,filter_date
from observe.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from django.urls import reverse
from observe.springs.forms import SpringForm
from django.contrib import messages
import statistics
import scipy.stats
from django.utils import timezone
from observe.utils.utils import render_to_pdf
import csv
import xlwt

################ Spring_inf
def spring_inf_update_form(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springinfnew = Spring_inf.objects.filter(xy_spring= xy_spring.pk).first()

    if request.method=="GET":
        form = Spring_infForm(instance=springinfnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/spring/springinf_form.html', context)
    elif request.method=="POST":
        form = Spring_infForm(request.POST,instance=springinfnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('xy_springs')
        else:
            messages.warning(request,'sorry the updated faild')
            return redirect('xy_springs')

################# add edit delete metology point


class SpringListView( BaseListView):
    model = XY_Spring
    paginate_by = 100  # if pagination is desired

class SpringCreate(LoginRequiredMixin, BaseCreateView):
    model = XY_Spring
    form_class = SpringForm

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        created_by = self.request.user
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'Your point was  saved successfully!')
        return super().form_valid(form)

class SpringUpdate( BaseUpdateView):
    model = XY_Spring
    form_class = SpringForm
    template_name = 'observe/spring_form.html'

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Your point was  updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        xy_spring = self.get_object()
        if self.request.user == xy_spring.created_by:
            return True
        else:
            return False

class SpringDelete( BaseDeleteView):
    model = XY_Spring

    def get_success_url(self):
        return reverse('xy_springs')

def all_xy_springs(request):
  XY_Springs = XY_Spring.objects.all()
  form = QueryForm(request.GET or None)
  paramDict = request.GET
  XY_Springs = filter_waterpoints(XY_Springs, paramDict)
  map_XY_Springs = serialize('geojson', XY_Springs)

  # print(map_waterpoints)
  context = {
        'XY_Springs': XY_Springs,
        'map_XY_Springs':map_XY_Springs,
        'form': form,
    }
  return render(request, 'observe/springs.html', context)



def import_spring_readings(request):
    XY_Springs = XY_Spring.objects.all()

    map_XY_Springs= serialize('geojson', XY_Springs)


    context = {
        'XY_Springs': XY_Springs,
        'map_XY_Springs': map_XY_Springs,

    }
    return render(request,'observe/spring_import_form.html',context)


##################### start spring_discharge_daily#############

def spring_sdd_list(request,id_field):

    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springinfnew = Spring_inf.objects.filter(xy_spring=xy_spring.pk).first()

    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))

    ###########springdischarge_dailys###############
    springdischarge_dailys = xy_spring.springdischarge_dailys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    springdischarge_dailys_new = filter_springdischarge_daily(springdischarge_dailys, paramDict)
    context={
        'springinfnew':springinfnew,
        'springdischarge_dailys_new':springdischarge_dailys_new,
        'id_field':id_field,
        'map_xy_spring':map_xy_spring,
        'form_date':form_date,
        'xy_spring':xy_spring,
    }
    return render(request,'observe/spring/spring_sdd_list.html',context)
def spring_sdd_create_form(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if (request.method=="POST") :
        form = spring_discharge_dailyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_spring
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'you add new reading successfully!')
            return redirect('sdd-list', id_field)
        else:
            messages.warning(request, 'sorry the new reading did not added .')

    elif (request.method=="GET") :
        form = spring_discharge_dailyForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/spring/sdd_form.html',context)
@user_is_springdischarge_daily_author
def spring_sdd_update_form(request, id_field ,id):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if request.method=="GET":
        springdischarge_dailynew = springdischarge_daily.objects.filter(pk=id).first()
        form = spring_discharge_dailyForm(instance=springdischarge_dailynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/spring/sdd_form.html', context)
    elif request.method=="POST":

        springdischarge_dailynew = springdischarge_daily.objects.filter(pk=id).first()
        form = spring_discharge_dailyForm(request.POST,instance=springdischarge_dailynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('sdd-list', id_field)
        else:
            messages.warning(request, 'sorry the updated did not do successfully.')
@login_required
def spring_sdd_Pdf(request,id_field):

    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    xy_spring_inf = xy_spring.spring_inf
    id_field =xy_spring.id_field
    springdischarge_dailys_new = xy_spring.springdischarge_dailys.filter(created_by=request.user)

    paramDict = request.GET
    springdischarge_dailys_new = filter_springdischarge_daily(springdischarge_dailys_new, paramDict)

    x = list()
    for entry in springdischarge_dailys_new:
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
        'springdischarge_dailys_new': springdischarge_dailys_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_spring_inf':xy_spring_inf,
        'xy_spring':xy_spring,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/spring/sdd_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
@user_is_springdischarge_daily_author
def spring_sdd_delete(request ,id_field,id):
    deleted_springdischarge_daily = springdischarge_daily.objects.get(pk=id)
    deleted_springdischarge_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdd-list', id_field)
@login_required
@user_is_springdischarge_daily_author
def spring_sdd_multi_delete(request,id_field):
    paramDict = request.GET
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springdischarge_dailys = xy_spring.springdischarge_dailys.filter(waterpoint_id=id_field)
    springdischarge_dailys = filter_springdischarge_daily(springdischarge_dailys, paramDict)

    paramDict = request.GET
    springdischarge_dailys = filter_springdischarge_daily(springdischarge_dailys, paramDict)
    for springdischarge_daily in springdischarge_dailys:
        springdischarge_daily.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdd-list', id_field)
@login_required
def export_spring_discharge_daily(request,id_field):
    spring_discharge_daily_resource = springdischarge_dailyResource()
    paramDict = request.GET
    spring_discharge_dailys = springdischarge_daily.objects.filter(waterpoint_id=id_field)
    spring_discharge_dailys = filter_springdischarge_daily(spring_discharge_dailys, paramDict)
    dataset = spring_discharge_daily_resource.export(spring_discharge_dailys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="spring_discharge_daily.xls"'
    return response
from tablib import Dataset

def simple_upload(request):
    if request.method == 'POST':
        springdischarge_daily_resource = springdischarge_dailyResource()
        dataset = Dataset()
        new_springdischarge_dailys = request.FILES['myfile']

        imported_data = dataset.load(new_springdischarge_dailys.read())
        result = springdischarge_daily_resource.imported_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            springdischarge_daily_resource.imported_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'observe/spring/spring_sdd_list.html')

#############spring discharge monthly#######333
@login_required
def spring_sdm_list(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springinfnew = Spring_inf.objects.filter(xy_spring= xy_spring.pk).first()

    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    springdischarge_monthlys = xy_spring.springdischarge_monthlys.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    springdischarge_monthlys_new = filter_springdischarge_monthly(springdischarge_monthlys, paramDict)
    context = {
        'springinfnew':springinfnew,
        'springdischarge_monthlys_new': springdischarge_monthlys_new,
        'id_field': id_field,
        'map_xy_spring': map_xy_spring,
        'form_date':form_date,
        'xy_spring':xy_spring
    }
    return render(request, 'observe/spring/spring_sdm_list.html', context)
@login_required
def spring_sdm_create_form(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if (request.method=="POST") :
        form = springdischarge_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_spring
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'you add new reading successfully!')
            return redirect('sdm-list', id_field)
        else:
            messages.warning(request, 'sorry the new reading did not added .')


    elif (request.method=="GET") :
        form = springdischarge_monthlyForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/spring/sdm_form.html',context)
@user_is_springdischarge_monthly_author
def spring_sdm_update_form(request, id_field ,id):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if request.method=="GET":
        springdischarge_monthlynew = springdischarge_monthly.objects.filter(pk=id).first()
        form = springdischarge_monthlyForm(instance=springdischarge_monthlynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/spring/sdm_form.html', context)
    elif request.method=="POST":

        springdischarge_monthlynew = springdischarge_monthly.objects.filter(pk=id).first()
        form = springdischarge_monthlyForm(request.POST,instance=springdischarge_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('sdm-list', id_field)
        else:
            messages.warning(request, 'sorry the updated did not do successfully.')
@login_required()
def spring_sdm_Pdf(request,id_field):

    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    xy_spring_inf = xy_spring.spring_inf
    id_field =xy_spring.id_field
    springdischarge_monthlys_new = xy_spring.springdischarge_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    springdischarge_monthlys_new = filter_springdischarge_monthly(springdischarge_monthlys_new, paramDict)

    x = list()
    for entry in springdischarge_monthlys_new:
     x.append(entry.monthly_avg_discharge)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'springdischarge_monthlys_new': springdischarge_monthlys_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_spring_inf':'xy_spring_inf',
        'xy_spring':xy_spring,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/spring/sdm_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_springdischarge_monthly_author
def spring_sdm_delete(request, id_field, id):
    deleted_springdischarge_monthly = springdischarge_monthly.objects.get(pk=id)
    deleted_springdischarge_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdm-list', id_field)

@user_is_springdischarge_monthly_author
def spring_sdm_multi_delete(request,id_field):
    paramDict = request.GET
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springdischarge_monthlys = xy_spring.springdischarge_monthlys.filter(waterpoint_id=id_field)
    springdischarge_monthlys = filter_springdischarge_monthly(springdischarge_monthlys, paramDict)

    paramDict = request.GET
    springdischarge_monthlys = filter_springdischarge_monthly(springdischarge_monthlys, paramDict)
    for springdischarge_monthly in springdischarge_monthlys:
        springdischarge_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdm-list', id_field)
@login_required()
def export_spring_discharge_monthly(request,id_field):
    spring_discharge_monthly_resource = springdischarge_monthlyResource()
    paramDict = request.GET
    springdischarge_monthlys = springdischarge_monthly.objects.filter(waterpoint_id=id_field)
    springdischarge_monthlys = filter_springdischarge_monthly(springdischarge_monthlys, paramDict)


    dataset = spring_discharge_monthly_resource.export(springdischarge_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="springdischarge_monthly.xls"'
    return response


#############spring discharge anually#######333
@login_required()
def spring_sda_list(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springinfnew = Spring_inf.objects.filter(xy_spring= xy_spring.pk).first()

    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    springdischarge_anuals = xy_spring.springdischarge_anuals.all()
    form_date = QueryDateAnnualForm(request.GET or None)
    paramDict = request.GET
    springdischarge_anuals_new = filter_springdischarge_anual(springdischarge_anuals, paramDict)
    context = {
        'springinfnew':springinfnew,
        'springdischarge_anuals_new': springdischarge_anuals_new,
        'id_field': id_field,
        'map_xy_spring': map_xy_spring,
        'form_date':form_date,
        'xy_spring':xy_spring
    }
    return render(request, 'observe/spring/spring_sda_list.html', context)
@login_required()
def spring_sda_create_form(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if (request.method=="POST") :
        form = springdischarge_anualForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_spring
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading  added successfully!')
            return redirect('sda-list', id_field)
        else:
            messages.warning(request, 'sorry the added faild !')
            return redirect('sda-list', id_field)

    elif (request.method=="GET") :
        form = springdischarge_anualForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/spring/sda_form.html',context)
@user_is_springdischarge_anual_author
def spring_sda_update_form(request, id_field ,id):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if request.method=="GET":
        springdischarge_anualnew = springdischarge_anual.objects.filter(pk=id).first()
        form = springdischarge_anualForm(instance=springdischarge_anualnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/spring/sda_form.html', context)
    elif request.method=="POST":

        springdischarge_anualnew = springdischarge_anual.objects.filter(pk=id).first()
        form = springdischarge_anualForm(request.POST,instance=springdischarge_anualnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('sda-list', id_field)
        else:
            messages.warning(request, 'sorry the updated faild!')
            return redirect('sda-list', id_field)
@login_required()
def spring_sda_Pdf(request,id_field):

    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    xy_spring_inf = xy_spring.spring_inf
    id_field =xy_spring.id_field
    springdischarge_anuals_new = xy_spring.springdischarge_anuals.filter(created_by=request.user)

    paramDict = request.GET
    springdischarge_anuals_new = filter_springdischarge_anual(springdischarge_anuals_new, paramDict)

    x = list()
    for entry in springdischarge_anuals_new:
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
        'springdischarge_anuals_new': springdischarge_anuals_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_spring_inf':xy_spring_inf,
        'xy_spring':xy_spring,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/spring/sda_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_springdischarge_anual_author
def spring_sda_delete(request, id_field, id):
    deleted_springdischarge_anual = springdischarge_anual.objects.get(pk=id)
    deleted_springdischarge_anual.delete()
    messages.success(request,'deleted done successfully !')
    return redirect('sda-list', id_field)
@user_is_springdischarge_anual_author

def spring_sda_multi_delete(request,id_field):
    paramDict = request.GET
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springdischarge_anuals = xy_spring.springdischarge_anuals.filter(waterpoint_id=id_field)
    springdischarge_anuals = filter_springdischarge_anual(springdischarge_anuals, paramDict)

    paramDict = request.GET
    springdischarge_anuals = filter_springdischarge_anual(springdischarge_anuals, paramDict)
    for springdischarge_anual in springdischarge_anuals:
        springdischarge_anual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sda-list', id_field)
@login_required()
def export_spring_discharge_anually(request,id_field):
    springdischarge_anual_resource = springdischarge_anualResource()
    paramDict = request.GET
    springdischarge_anuals = springdischarge_anual.objects.filter(waterpoint_id=id_field)
    springdischarge_anuals = filter_springdischarge_anual(springdischarge_anuals, paramDict)


    dataset = springdischarge_anual_resource.export(springdischarge_anuals)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="springdischarge_anual.xls"'
    return response

#############spring discharge avg anually#######333
@login_required()
def spring_sdaa_list(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springinfnew = Spring_inf.objects.filter(xy_spring= xy_spring.pk).first()

    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    springdischarge_avg_anuals = xy_spring.springdischarge_avg_anuals.all()
    form_date = QueryDateForm(request.GET or None)
    paramDict = request.GET
    springdischarge_avg_anuals_new = filter_springdischarge_avg_anual(springdischarge_avg_anuals, paramDict)
    context = {
        'springinfnew':springinfnew,
        'springdischarge_avg_anuals_new': springdischarge_avg_anuals_new,
        'id_field': id_field,
        'map_xy_spring': map_xy_spring,
        'form_date':form_date,
        'xy_spring':xy_spring,
    }
    return render(request, 'observe/spring/spring_sdaa_list.html', context)
@login_required()
def spring_sdaa_create_form(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if (request.method=="POST") :
        form = springdischarge_avg_anualForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_spring
            new_form.created_by = request.user
            new_form.save()
            messages.success(request,'the new reading added successfully !')
            return redirect('sdaa-list', id_field)
        else:
            messages.success(request, 'sorry the added faild !')
            return redirect('sdaa-list', id_field)

    elif (request.method=="GET") :
        form = springdischarge_avg_anualForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/spring/sdaa_form.html',context)
@user_is_springdischarge_avg_anual_author
def spring_sdaa_update_form(request, id_field ,id):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if request.method=="GET":
        springdischarge_avg_anualnew = springdischarge_avg_anual.objects.filter(pk=id).first()
        form = springdischarge_avg_anualForm(instance=springdischarge_avg_anualnew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/spring/sdaa_form.html', context)
    elif request.method=="POST":

        springdischarge_avg_anualnew = springdischarge_avg_anual.objects.filter(pk=id).first()
        form = springdischarge_avg_anualForm(request.POST,instance=springdischarge_avg_anualnew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')
            return redirect('sdaa-list', id_field)
        else:
            messages.success(request, 'sorry the updated faild!')
            return redirect('sdaa-list', id_field)
@login_required()
def spring_sdaa_Pdf(request,id_field):

    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    xy_spring_inf = xy_spring.spring_inf
    id_field =xy_spring.id_field
    springdischarge_avg_anuals_new = xy_spring.springdischarge_avg_anuals.filter(created_by=request.user)

    paramDict = request.GET
    springdischarge_avg_anuals_new = filter_springdischarge_avg_anual(springdischarge_avg_anuals_new, paramDict)

    x = list()
    for entry in springdischarge_avg_anuals_new:
     x.append(entry.avg_discharge)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'springdischarge_avg_anuals_new': springdischarge_avg_anuals_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_spring_inf':xy_spring_inf,
        'xy_spring':xy_spring,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/spring/sdaa_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

@user_is_springdischarge_avg_anual_author
def spring_sdaa_delete(request, id_field, id):
    deleted_springdischarge_avg_anual = springdischarge_avg_anual.objects.get(pk=id)
    deleted_springdischarge_avg_anual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdaa-list', id_field)
@user_is_springdischarge_avg_anual_author
def spring_sdaa_multi_delete(request,id_field):
    paramDict = request.GET
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springdischarge_avg_anuals = xy_spring.springdischarge_avg_anuals.filter(waterpoint_id=id_field)
    springdischarge_avg_anuals = filter_springdischarge_avg_anual(springdischarge_avg_anuals, paramDict)

    paramDict = request.GET
    springdischarge_avg_anuals = filter_springdischarge_avg_anual(springdischarge_avg_anuals, paramDict)
    for springdischarge_avg_anual in springdischarge_avg_anuals:
        springdischarge_avg_anual.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdaa-list', id_field)
@login_required()
def export_spring_discharge_avg_anually(request,id_field):
    springdischarge_avg_anual_resource = springdischarge_avg_anualResource()
    paramDict = request.GET
    springdischarge_avg_anuals = springdischarge_avg_anual.objects.filter(waterpoint_id=id_field)
    springdischarge_avg_anuals = filter_springdischarge_avg_anual(springdischarge_avg_anuals, paramDict)
    dataset = springdischarge_avg_anual_resource.export(springdischarge_avg_anuals)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="springdischarge_avg_anual.xls"'
    return response


#############spring discharge avg monthly#######333
@login_required()
def spring_sdam_list(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springinfnew = Spring_inf.objects.filter(xy_spring= xy_spring.pk).first()

    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    springdischarge_avg_monthlys = xy_spring.springdischarge_avg_monthlys.all()
    form_date = QueryDateMonthForm(request.GET or None)
    paramDict = request.GET
    springdischarge_avg_monthlys_new = filter_springdischarge_avg_monthly(springdischarge_avg_monthlys, paramDict)
    context = {
        'springinfnew':springinfnew,
        'springdischarge_avg_monthlys_new': springdischarge_avg_monthlys_new,
        'id_field': id_field,
        'map_xy_spring': map_xy_spring,
        'form_date':form_date,
        'xy_spring':xy_spring
    }
    return render(request, 'observe/spring/spring_sdam_list.html', context)
@login_required()
def spring_sdam_create_form(request, id_field):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if (request.method=="POST") :
        form = springdischarge_avg_monthlyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.waterpoint = xy_spring
            new_form.created_by = request.user
            new_form.save()
            messages.success(request, 'the new reading  added successfully!')

            return redirect('sdam-list', id_field)
        else:
            messages.warning(request, 'sorry the added faild !')


    elif (request.method=="GET") :
        form = springdischarge_avg_monthlyForm()

    context={
            'form':form,
        'id_field':id_field}

    return render(request, 'observe/spring/sdam_form.html',context)
@user_is_springdischarge_avg_monthly_author

def spring_sdam_update_form(request, id_field ,id):
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    if request.method=="GET":
        springdischarge_avg_monthlynew = springdischarge_avg_monthly.objects.filter(pk=id).first()
        form = springdischarge_avg_monthlyForm(instance=springdischarge_avg_monthlynew)
        context = {
            'form': form,
            'id_field': id_field
        }
        return render(request, 'observe/spring/sdam_form.html', context)
    elif request.method=="POST":

        springdischarge_avg_monthlynew = springdischarge_avg_monthly.objects.filter(pk=id).first()
        form = springdischarge_avg_monthlyForm(request.POST,instance=springdischarge_avg_monthlynew)
        if form.is_valid():
            form.save()
            messages.success(request, 'the updated done successfully!')

            return redirect('sdam-list', id_field)
        else:
            messages.warning(request, 'sorry the updated faild!')
            return redirect('sdam-list', id_field)

@login_required()
def spring_sdam_Pdf(request,id_field):

    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    map_xy_spring = serialize('geojson', XY_Spring.objects.filter(pk=id_field))
    xy_spring_inf = xy_spring.spring_inf
    id_field =xy_spring.id_field
    springdischarge_avg_monthlys_new = xy_spring.springdischarge_avg_monthlys.filter(created_by=request.user)

    paramDict = request.GET
    springdischarge_avg_monthlys_new = filter_springdischarge_avg_anual(springdischarge_avg_monthlys_new, paramDict)

    x = list()
    for entry in springdischarge_avg_monthlys_new:
     x.append(entry.avg_discharge)
    mean_x = statistics.mean(x)
    median_x = statistics.median(x)
    mode_x = statistics.multimode(x)
    max_x = max(x)
    min_x = min(x)
    count_x = len(x)
    today = timezone.now()

    params = {
        'today': today,
        'springdischarge_avg_monthlys_new': springdischarge_avg_monthlys_new,
         'mean_x':mean_x,
        'count_x':count_x,
        'xy_spring_inf':'xy_spring_inf',
        'xy_spring':xy_spring,
        'max_x':max_x,
        'min_x':min_x,
        'median_x':median_x,
        'mode_x':mode_x,
        'mean_x':mean_x,
    }
    pdf = render_to_pdf('observe/spring/sdam_report.html', params)
    return HttpResponse(pdf, content_type='application/pdf')
@user_is_springdischarge_avg_monthly_author
def spring_sdam_delete(request, id_field, id):
    deleted_springdischarge_avg_monthly = springdischarge_avg_monthly.objects.get(pk=id)
    deleted_springdischarge_avg_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdam-list', id_field)
@user_is_springdischarge_avg_monthly_author

def spring_sdam_multi_delete(request,id_field):
    paramDict = request.GET
    xy_spring = get_object_or_404(XY_Spring, pk=id_field)
    springdischarge_avg_monthlys = xy_spring.springdischarge_avg_monthlys.filter(waterpoint_id=id_field)
    springdischarge_avg_monthlys = filter_springdischarge_avg_monthly(springdischarge_avg_monthlys, paramDict)

    paramDict = request.GET
    springdischarge_avg_monthlys = filter_springdischarge_avg_monthly(springdischarge_avg_monthlys, paramDict)
    for springdischarge_avg_monthly in springdischarge_avg_monthlys:
        springdischarge_avg_monthly.delete()
    messages.success(request, 'the deleted done successfully!')
    return redirect('sdam-list', id_field)
@login_required()
def export_spring_discharge_avg_monthly(request,id_field):
    springdischarge_avg_monthly_resource = springdischarge_avg_monthlyResource()
    paramDict = request.GET
    springdischarge_avg_monthlys= springdischarge_avg_monthly.objects.filter(waterpoint_id=id_field)
    springdischarge_avg_monthlys = filter_springdischarge_avg_monthly(springdischarge_avg_monthlys, paramDict)


    dataset = springdischarge_avg_monthly_resource.export(springdischarge_avg_monthlys)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="springdischarge_avg_monthly.xls"'
    return response



@login_required()
def export_filtered_springs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="waterpoints.csv"'

    writer = csv.writer(response)
    writer.writerow(['id_field',   'old_id',    'sitename_a',   'sitename_e',    'type',   'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y'])
    waterpoints = XY_Spring.objects.all()
    paramDict = request.GET
    waterpoints = filter_waterpoints(waterpoints, paramDict)
    waterpoints = waterpoints.values_list(
        'id_field',   'old_id',    'sitename_a',   'sitename_e',    'type',   'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y')

    for waterpoint in waterpoints:
        writer.writerow(waterpoint)

    return response
@login_required()
def export_filtered_springs_xls(request):
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


    rows = XY_Spring.objects.all().values_list('id_field',   'old_id',    'sitename_a', 'sitename_e', 'type', 'agency',   'mohafaza',   'montika',   'nahia',   'village',
        'sub_baisn',    'w84_utm_x',    'w84_utm_y',	'w84_utm_z',	'means_z',	'stm_x','stm_y')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

