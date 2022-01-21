from django import forms
from observe.models import geophysicalproject,geophysicalsurvey,vertical_electric_sounding,ves_result_ap,\
    ves_result_sp,profiling_electric_sounding_re,profiling_electric_sounding_da



class geophysicalprojectForm(forms.ModelForm):

    class Meta:
        model = geophysicalproject
        fields = '__all__'

class geophysicalsurveyForm(forms.ModelForm):

    class Meta:
        model = geophysicalsurvey
        fields = '__all__'

class vertical_electric_soundingForm(forms.ModelForm):

    class Meta:
        model = vertical_electric_sounding
        fields = '__all__'

class ves_result_apForm(forms.ModelForm):

    class Meta:
        model = ves_result_ap
        fields = '__all__'

class ves_result_spForm(forms.ModelForm):

    class Meta:
        model = ves_result_sp
        fields = '__all__'

class profiling_electric_sounding_reForm(forms.ModelForm):

    class Meta:
        model = profiling_electric_sounding_re
        fields = '__all__'

class profiling_electric_sounding_daForm(forms.ModelForm):

    class Meta:
        model = profiling_electric_sounding_da
        fields = '__all__'
