from django.core.serializers import serialize
from django.shortcuts import render,get_object_or_404,redirect
from observe.wells.models import XY_Well
from observe.pumpings.forms import pumpingForm,pumptest_obswellForm,step_drawdownForm,pumptest_pumpwellForm,continious_dischageForm,recovery_testForm,WaterpointForm
from observe.models import pumping,pumptest_obswell,step_drawdown,continious_dischage,recovery_test,Waterpoint,pumptest_pumpwell



from django.contrib import messages
from observe.models import Waterpoint
from django.urls import reverse

from observe.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView

def all_waterpoint_pump(request):
  xy_waterpoints = Waterpoint.objects.all()
  map_xy_waterpoints = serialize('geojson', xy_waterpoints)

  context = {
        'xy_waterpoints': xy_waterpoints,
        'map_xy_waterpoints':map_xy_waterpoints,

    }
  return render(request, 'observe/waterpoints.html', context)

class WaterpointListView( BaseListView):
    model = Waterpoint
    paginate_by = 100  # if pagination is desired

class WaterpointCreate( BaseCreateView):
    model = Waterpoint
    form_class = WaterpointForm

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Your point was  saved successfully!')
        return super().form_valid(form)

class WaterpointUpdate( BaseUpdateView):
    model = Waterpoint
    form_class = WaterpointForm
    template_name = 'observe/waterpoint_form.html'

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Your point was  updated successfully!')
        return super().form_valid(form)

class WaterpointDelete( BaseDeleteView):
    model = Waterpoint
    def get_success_url(self):
        return reverse('waterpoints')

#################
def pumping_pmp_list(request,waterpoint_id):
    waterpoint = get_object_or_404(Waterpoint, pk=waterpoint_id)
    map_waterpoint = serialize('geojson', Waterpoint.objects.filter(pk=waterpoint_id))
    # print(map_waterpoint)
    newpumpings = waterpoint.pumpings.all()

    context={
        'newpumpings':newpumpings,
        'waterpoint_id':waterpoint_id,
        'map_waterpoint':map_waterpoint
    }
    return render(request,'observe/pumping/pumping_pump_list.html',context)

def pumping_pmp_form(request, waterpoint_id ,id=0):
    waterpoint = get_object_or_404(Waterpoint, pk=waterpoint_id)

    if request.method=="GET":
        if id==0:
            form = pumpingForm()
        else:
            pumpingnew = pumping.objects.filter(pk=id).first()
            form = pumpingForm(instance=pumpingnew)
        context = {'form': form,'waterpoint_id':waterpoint_id}
        return render(request, 'observe/pumping/pumping_pump_form.html',context)
    else:
        if id==0:
            form = pumpingForm(request.POST)
            new_form = form.save(commit=False)
            new_form.waterpoint = waterpoint
            new_form.save()
        else:
            pumpingnew = pumping.objects.filter(pk=id).first()
            form = pumpingForm(request.POST,instance=pumpingnew)
        if form.is_valid():
            form.save()
        return redirect('pump-list', waterpoint_id)

def pumping_pmp_delete(request ,waterpoint_id,id):
    deleted_pumping = pumping.objects.get(pk=id)
    deleted_pumping.delete()
    return redirect('pump-list', waterpoint_id)

#####################
def pumptest_obswell_list(request,pumping_id):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    waterpoint_id = pumpingnew.waterpoint.id

    pumptest_obswells = pumpingnew.pumptest_obswells.all()

    context = {
        'pumptest_obswells': pumptest_obswells,
        'pumping_id': pumping_id,
        'waterpoint_id':waterpoint_id

    }
    return render(request, 'observe/pumping/pumptest_obswell_list.html', context)


def pumptest_obswell_form(request, pumping_id, id=0):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)

    if request.method == "GET":
        if id == 0:
            form = pumptest_obswellForm()
        else:
            pumptest_obswellnew = pumptest_obswell.objects.filter(pk=id).first()
            form = pumptest_obswellForm(instance=pumptest_obswellnew)
        context = {'form': form, 'pumping_id': pumping_id}
        return render(request, 'observe/pumping/pumptest_obswell_form.html', context)
    else:
        if id == 0:
            form = pumptest_obswellForm(request.POST)
            new_form = form.save(commit=False)
            new_form.pumping = pumpingnew
            new_form.save()
        else:
            pumptest_obswellnew1 = pumptest_obswell.objects.filter(pk=id).first()
            form = pumptest_obswellForm(request.POST, instance=pumptest_obswellnew1)
        if form.is_valid():
            form.save()
        return redirect('pump-obswell-list', pumping_id)


def pumptest_obswell_delete(request, pumping_id, id):
    deleted_pumptest_obswell = pumptest_obswell.objects.get(pk=id)
    deleted_pumptest_obswell.delete()
    return redirect('pump-obswell-list', pumping_id)

###################
def pumptest_pumpwell_list(request, pumping_id):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    pumptest_pumpwells = pumpingnew.pumptest_pumpwells.all()
    waterpoint_id = pumpingnew.waterpoint.id
    context = {
        'pumptest_pumpwells': pumptest_pumpwells,
        'pumping_id': pumping_id,
        'waterpoint_id':waterpoint_id

    }
    return render(request, 'observe/pumping/pumptest_pumpwell_list.html', context)


def pumptest_pumpwell_form(request, pumping_id, id=0):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)

    if request.method == "GET":
        if id == 0:
            form = pumptest_pumpwellForm()
        else:
            pumptest_pumpwellnew = pumptest_pumpwell.objects.filter(pk=id).first()
            form = pumptest_pumpwellForm(instance=pumptest_pumpwellnew)
        context = {'form': form, 'pumping_id': pumping_id}
        return render(request, 'observe/pumping/pumptest_pumpwell_form.html', context)
    else:
        if id == 0:
            form = pumptest_pumpwellForm(request.POST)
            new_form = form.save(commit=False)
            new_form.pumping = pumpingnew
            new_form.save()

        else:
            pumptest_pumpwellnew2 = pumptest_pumpwell.objects.filter(pk=id).first()
            form = pumptest_pumpwellForm(request.POST, instance=pumptest_pumpwellnew2)
        if form.is_valid():
            form.save()
        return redirect('pump-pumpwell-list', pumping_id)


def pumptest_pumpwell_delete(request, pumping_id, id):
    deleted_pumptest_pumpwell = pumptest_pumpwell.objects.get(pk=id)
    deleted_pumptest_pumpwell.delete()
    return redirect('pump-pumpwell-list', pumping_id)

############

def step_drawdown_list(request, pumping_id):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    step_drawdowns = pumpingnew.step_drawdowns.all()
    waterpoint_id = pumpingnew.waterpoint.id
    context = {
        'step_drawdowns': step_drawdowns,
        'pumping_id': pumping_id,
        'waterpoint_id':waterpoint_id

    }
    return render(request, 'observe/pumping/step_drawdown_list.html', context)


def step_drawdown_form(request, pumping_id, id=0):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    if request.method == "GET":
        if id == 0:
            form = step_drawdownForm()
        else:
            step_drawdownnew = step_drawdown.objects.filter(pk=id).first()
            form = step_drawdownForm(instance=step_drawdownnew)
        context = {'form': form, 'pumping_id': pumping_id}
        return render(request, 'observe/pumping/step_drawdown_form.html', context)
    else:
        if id == 0:
            form = step_drawdownForm(request.POST)
            new_form = form.save(commit=False)
            new_form.pumping = pumpingnew
            new_form.save()

        else:
            step_drawdownnew2 = step_drawdown.objects.filter(pk=id).first()
            form = step_drawdownForm(request.POST, instance=step_drawdownnew2)
        if form.is_valid():
            form.save()

        return redirect('step-drawdown-list', pumping_id)


def step_drawdown_delete(request, pumping_id, id):
    deleted_step_drawdown = step_drawdown.objects.get(pk=id)
    deleted_step_drawdown.delete()
    return redirect('step-drawdown-list', pumping_id)

##################
def continious_dischage_list(request, pumping_id):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    continious_dischages = pumpingnew.continious_dischages.all()
    waterpoint_id = pumpingnew.waterpoint.id

    context = {
        'continious_dischages': continious_dischages,
        'pumping_id': pumping_id,
        'waterpoint_id':waterpoint_id

    }
    return render(request, 'observe/pumping/fieldparameter_list.html', context)


def continious_dischage_form(request, pumping_id, id=0):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)

    if request.method == "GET":
        if id == 0:
            form = continious_dischageForm()
        else:
            continious_dischagenew = continious_dischage.objects.filter(pk=id).first()
            form = continious_dischageForm(instance=continious_dischagenew)
        context = {'form': form, 'pumping_id': pumping_id}
        return render(request, 'observe/pumping/fieldparameter_form.html', context)
    else:
        if id == 0:
            form = continious_dischageForm(request.POST)
            new_form = form.save(commit=False)
            new_form.pumping = pumpingnew
            new_form.save()

        else:
            continious_dischagenew2 = continious_dischage.objects.filter(pk=id).first()
            form = continious_dischageForm(request.POST, instance=continious_dischagenew2)
        if form.is_valid():
            form.save()
        return redirect('continious-dischage-list', pumping_id)


def continious_dischage_delete(request, pumping_id, id):
    deleted_continious_dischage = continious_dischage.objects.get(pk=id)
    deleted_continious_dischage.delete()
    return redirect('continious-dischage-list', pumping_id)

########################

def recovery_test_list(request, pumping_id):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    recovery_tests = pumpingnew.recovery_tests.all()
    waterpoint_id = pumpingnew.waterpoint.id

    context = {
        'recovery_tests': recovery_tests,
        'pumping_id': pumping_id,
        'waterpoint_id':waterpoint_id

    }
    return render(request, 'observe/pumping/recovery_test_list.html', context)


def recovery_test_form(request, pumping_id, id=0):
    pumpingnew = get_object_or_404(pumping, pk=pumping_id)
    if request.method == "GET":
        if id == 0:
            form = recovery_testForm()
        else:
            recovery_testnew = recovery_test.objects.filter(pk=id).first()
            form = recovery_testForm(instance=recovery_testnew)
        context = {'form': form, 'pumping_id': pumping_id}
        return render(request, 'observe/pumping/recovery_test_form.html', context)
    else:
        if id == 0:
            form = recovery_testForm(request.POST)
            new_form = form.save(commit=False)
            new_form.pumping = pumpingnew
            new_form.save()

        else:
            recovery_testnew2 = recovery_test.objects.filter(pk=id).first()
            form = recovery_testForm(request.POST, instance=recovery_testnew2)
        if form.is_valid():
            form.save()
        return redirect('recovery-test-list', pumping_id)


def recovery_test_delete(request, pumping_id, id):
    deleted_recovery_test = recovery_test.objects.get(pk=id)
    deleted_recovery_test.delete()
    return redirect('recovery-test-list', pumping_id)

#####################