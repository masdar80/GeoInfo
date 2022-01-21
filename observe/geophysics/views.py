from django.shortcuts import render,get_object_or_404,redirect
from observe.models import geophysicalproject,geophysicalsurvey,vertical_electric_sounding,ves_result_ap,ves_result_sp,\
    profiling_electric_sounding_da,profiling_electric_sounding_re
from observe.geophysics.forms import geophysicalprojectForm,geophysicalsurveyForm,vertical_electric_soundingForm,ves_result_spForm,\
    ves_result_apForm,profiling_electric_sounding_reForm,profiling_electric_sounding_daForm,geophysicalproject
#########
def geophysicalproject_list(request):

    geophysicalprojects = geophysicalproject.objects.all()

    context={
        'geophysicalprojects':geophysicalprojects,
    }
    return render(request,'observe/geophysical/geophysicalproject_list.html',context)

def geophysicalproject_form(request, id=0):

    if request.method=="GET":
        if id==0:
            form = geophysicalprojectForm()
        else:
            geophysicalprojectnew = geophysicalproject.objects.filter(pk=id).first()
            form = geophysicalprojectForm(instance=geophysicalprojectnew)
        context = {'form': form}
        return render(request, 'observe/geophysical/geophysicalproject_form.html',context)
    else:
        if id==0:
            form = geophysicalprojectForm(request.POST)

            form.save()
        else:
            geophysicalprojectnew = geophysicalproject.objects.filter(pk=id).first()
            form = geophysicalprojectForm(request.POST,instance=geophysicalprojectnew)
        if form.is_valid():
            form.save()
        return redirect('geophysicalproject-list')

def geophysicalproject_delete(request ,id):
    deleted_geophysicalproject = geophysicalproject.objects.get(pk=id)
    deleted_geophysicalproject.delete()
    return redirect('geophysicalproject-list')

#################

def geophysicalsurvey_list(request, geophysicalproject_id):
    geophysicalproject_new = get_object_or_404(geophysicalproject, pk=geophysicalproject_id)
    geophysicalsurveys = geophysicalproject_new.geophysicalsurveys.all()


    context = {
        'geophysicalsurveys': geophysicalsurveys,
        'geophysicalproject_id':'geophysicalproject_id'
    }
    return render(request, 'observe/geophysical/geophysicalproject_list.html', context)


def geophysicalsurvey_form(request, geophysicalproject_id,id=0):
    geophysicalprojectnew = get_object_or_404(geophysicalproject, pk=geophysicalproject_id)
    if request.method == "GET":
        if id == 0:
            form = geophysicalsurveyForm()
        else:
            geophysicalsurveynew = geophysicalsurvey.objects.filter(pk=id).first()
            form = geophysicalsurveyForm(instance=geophysicalsurveynew)
        context = {'form': form}
        return render(request, 'observe/geophysical/geophysicalsurvey_form.html', context)
    else:
        if id == 0:
            form = geophysicalsurveyForm(request.POST)
            new_form = form.save(commit=False)
            new_form.geophysicalproject = geophysicalprojectnew
            new_form.save()
        else:
            geophysicalsurveynew = geophysicalsurvey.objects.filter(pk=id).first()
            form = geophysicalsurveyForm(request.POST, instance=geophysicalsurveynew)
        if form.is_valid():
            form.save()
        return redirect('geophysicalsurvey-list')


def geophysicalsurvey_delete(request, id):
    deleted_geophysicalsurvey = geophysicalsurvey.objects.get(pk=id)
    deleted_geophysicalsurvey.delete()
    return redirect('geophysicalsurvey-list')

####################

def vertical_electric_sounding_list(request, geophysicalsurvey_id):
    geophysicalsurvey_new = get_object_or_404(geophysicalsurvey, pk=geophysicalsurvey_id)
    vertical_electric_soundings = geophysicalsurvey_new.vertical_electric_soundings.all()


    context = {
        'vertical_electric_soundings': vertical_electric_soundings,
        'geophysicalsurvey_id':'geophysicalsurvey_id'
    }
    return render(request, 'observe/geophysical/vertical_electric_sounding_list.html', context)


def vertical_electric_sounding_form(request, geophysicalsurvey_id,id=0):
    geophysicalsurveynew = get_object_or_404(geophysicalsurvey, pk=geophysicalsurvey_id)
    if request.method == "GET":
        if id == 0:
            form = vertical_electric_soundingForm()
        else:
            vertical_electric_soundingnew = vertical_electric_sounding.objects.filter(pk=id).first()
            form = vertical_electric_soundingForm(instance=vertical_electric_soundingnew)
        context = {'form': form,'geophysicalsurveynew':geophysicalsurveynew}
        return render(request, 'observe/geophysical/vertical_electric_sounding_form.html', context)
    else:
        if id == 0:
            form = vertical_electric_soundingForm(request.POST)
            new_form = form.save(commit=False)
            new_form.geophysicalsurvey = geophysicalsurvey
            new_form.save()
        else:
            vertical_electric_soundingnew = vertical_electric_sounding.objects.filter(pk=id).first()
            form = vertical_electric_soundingForm(request.POST, instance=vertical_electric_soundingnew)
        if form.is_valid():
            form.save()
        return redirect('vertical-electric-sounding-list')


def vertical_electric_sounding_delete(request, id):
    deleted_vertical_electric_sounding = vertical_electric_sounding.objects.get(pk=id)
    deleted_vertical_electric_sounding.delete()
    return redirect('vertical-electric-sounding-list')
#############

def profiling_electric_sounding_re_list(request, geophysicalsurvey_id):
    geophysicalsurvey_new = get_object_or_404(geophysicalsurvey, pk=geophysicalsurvey_id)
    profiling_electric_sounding_res = geophysicalsurvey_new.profiling_electric_sounding_re.all()


    context = {
        'profiling_electric_sounding_res': profiling_electric_sounding_res,
        'geophysicalsurvey_id':'geophysicalsurvey_id'
    }
    return render(request, 'observe/geophysical/profiling_electric_sounding_re_list.html', context)


def profiling_electric_sounding_re_form(request, geophysicalsurvey_id,id=0):
    geophysicalsurveynew = get_object_or_404(geophysicalsurvey, pk=geophysicalsurvey_id)
    if request.method == "GET":
        if id == 0:
            form = profiling_electric_sounding_reForm()
        else:
            profiling_electric_sounding_renew = profiling_electric_sounding_re.objects.filter(pk=id).first()
            form = profiling_electric_sounding_reForm(instance=profiling_electric_sounding_renew)
        context = {'form': form,'geophysicalsurveynew':geophysicalsurveynew}
        return render(request, 'observe/geophysical/profiling_electric_sounding_re_form.html', context)
    else:
        if id == 0:
            form = profiling_electric_sounding_reForm(request.POST)
            new_form = form.save(commit=False)
            new_form.geophysicalsurvey = geophysicalsurvey
            new_form.save()
        else:
            profiling_electric_sounding_renew = profiling_electric_sounding_re.objects.filter(pk=id).first()
            form = profiling_electric_sounding_reForm(request.POST, instance=profiling_electric_sounding_renew)
        if form.is_valid():
            form.save()
        return redirect('profiling-electric-sounding-re-list')


def profiling_electric_sounding_re_delete(request, id):
    deleted_profiling_electric_sounding_re = profiling_electric_sounding_re.objects.get(pk=id)
    deleted_profiling_electric_sounding_re.delete()
    return redirect('deleted-profiling-electric-sounding-re-list')

#######

def profiling_electric_sounding_da_list(request, profiling_electric_sounding_re_id):
    profiling_electric_sounding_re_new = get_object_or_404(profiling_electric_sounding_re, pk=profiling_electric_sounding_re_id)
    profiling_electric_sounding_das = profiling_electric_sounding_re_new.profiling_electric_sounding_das.all()


    context = {
        'profiling_electric_sounding_das': profiling_electric_sounding_das,
        'profiling_electric_sounding_re_id':'profiling_electric_sounding_re_id'
    }
    return render(request, 'observe/geophysical/profiling_electric_sounding_da_list.html', context)


def profiling_electric_sounding_da_form(request, profiling_electric_sounding_re_id,id=0):
    profiling_electric_sounding_renew = get_object_or_404(profiling_electric_sounding_re, pk=profiling_electric_sounding_re_id)
    if request.method == "GET":
        if id == 0:
            form = profiling_electric_sounding_daForm()
        else:
            profiling_electric_sounding_danew = profiling_electric_sounding_da.objects.filter(pk=id).first()
            form = profiling_electric_sounding_daForm(instance=profiling_electric_sounding_danew)
        context = {'form': form,'profiling_electric_sounding_renew':profiling_electric_sounding_renew}
        return render(request, 'observe/geophysical/profiling_electric_sounding_da_form.html', context)
    else:
        if id == 0:
            form = profiling_electric_sounding_daForm(request.POST)
            new_form = form.save(commit=False)
            new_form.profiling_electric_sounding_re = profiling_electric_sounding_renew
            new_form.save()
        else:
            profiling_electric_sounding_danew = profiling_electric_sounding_da.objects.filter(pk=id).first()
            form = profiling_electric_sounding_daForm(request.POST, instance=profiling_electric_sounding_danew)
        if form.is_valid():
            form.save()
        return redirect('profiling-electric-sounding-da-list')


def profiling_electric_sounding_da_delete(request, id):
    deleted_profiling_electric_sounding_da = profiling_electric_sounding_da.objects.get(pk=id)
    deleted_profiling_electric_sounding_da.delete()
    return redirect('deleted-profiling-electric-sounding-da-list')

#######

def ves_result_ap_list(request, vertical_electric_sounding_id):
    vertical_electric_sounding_new = get_object_or_404(vertical_electric_sounding, pk=vertical_electric_sounding_id)
    ves_result_aps = vertical_electric_sounding_new.ves_result_aps.all()


    context = {
        'ves_result_aps': ves_result_aps,
        'vertical_electric_sounding_id':'vertical_electric_sounding_id'
    }
    return render(request, 'observe/geophysical/ves_result_ap_list.html', context)


def ves_result_ap_form(request, vertical_electric_sounding_id,id=0):
    vertical_electric_soundingnew = get_object_or_404(vertical_electric_sounding, pk=vertical_electric_sounding_id)
    if request.method == "GET":
        if id == 0:
            form = ves_result_apForm()
        else:
            ves_result_apnew = ves_result_ap.objects.filter(pk=id).first()
            form = ves_result_apForm(instance=ves_result_apnew)
        context = {'form': form,'vertical_electric_soundingnew':vertical_electric_soundingnew}
        return render(request, 'observe/geophysical/ves_result_ap_form.html', context)
    else:
        if id == 0:
            form = ves_result_apForm(request.POST)
            new_form = form.save(commit=False)
            new_form.vertical_electric_sounding = vertical_electric_soundingnew
            new_form.save()
        else:
            ves_result_apnew = ves_result_ap.objects.filter(pk=id).first()
            form = ves_result_apForm(request.POST, instance=ves_result_apnew)
        if form.is_valid():
            form.save()
        return redirect('ves-result-ap-list')


def ves_result_ap_delete(request, id):
    deleted_ves_result_ap = ves_result_ap.objects.get(pk=id)
    deleted_ves_result_ap.delete()
    return redirect('ves-result-ap-list')

###############

def ves_result_sp_list(request, vertical_electric_sounding_id):
    vertical_electric_sounding_new = get_object_or_404(vertical_electric_sounding, pk=vertical_electric_sounding_id)
    ves_result_sps = vertical_electric_sounding_new.ves_result_sps.all()


    context = {
        'ves_result_sps': ves_result_sps,
        'vertical_electric_sounding_id':'vertical_electric_sounding_id',
        'vertical_electric_sounding_new':vertical_electric_sounding_new
    }
    return render(request, 'observe/geophysical/ves_result_sp_list.html', context)


def ves_result_sp_form(request, vertical_electric_sounding_id,id=0):
    vertical_electric_soundingnew = get_object_or_404(vertical_electric_sounding, pk=vertical_electric_sounding_id)
    if request.method == "GET":
        if id == 0:
            form = ves_result_spForm()
        else:
            ves_result_spnew = ves_result_sp.objects.filter(pk=id).first()
            form = ves_result_apForm(instance=ves_result_spnew)
        context = {'form': form,'vertical_electric_soundingnew':vertical_electric_soundingnew}
        return render(request, 'observe/geophysical/ves_result_sp_form.html', context)
    else:
        if id == 0:
            form = ves_result_spForm(request.POST)
            new_form = form.save(commit=False)
            new_form.vertical_electric_sounding = vertical_electric_soundingnew
            new_form.save()
        else:
            ves_result_spnew = ves_result_sp.objects.filter(pk=id).first()
            form = ves_result_spForm(request.POST, instance=ves_result_spnew)
        if form.is_valid():
            form.save()
        return redirect('ves-result-sp-list')


def ves_result_sp_delete(request, id):
    deleted_ves_result_sp = ves_result_sp.objects.get(pk=id)
    deleted_ves_result_sp.delete()
    return redirect('ves-result-sp-list')
###############
