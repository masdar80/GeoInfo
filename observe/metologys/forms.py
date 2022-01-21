from django import forms
from observe.metologys.models import precipitation_daily,precipitation_monthly,precipitation_annual,temperature_daily,temperature_monthly,\
    evaporation_daily,evaporation_monthly,humidity_daily,humidity_monthly,airpressure,wind_monthly,wind_daily,sunshine_daily,Metology_inf,\
snowdepth,snowfall
from observe.metologys.models import XY_Metology
from leaflet.forms.widgets import LeafletWidget

class QueryForm(forms.Form):
    keywords = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(

            attrs={
                'class': 'form-control',
                'placeholder': 'space-separated words matching  sitename_e, mohafaza, montika, id_field, village, sub_baisn, type'
            }))

    obs_datetime_before = forms.DateField(
        label='',
        required=False,
        # initial = datetime.datetime.now(),

        widget=forms.DateInput(
            format='yyyy-mm-dd',

            attrs={
                'class': 'form-control',
                'id': 'datepicker1',
                'placeholder': 'published before'
            }

        ))

    obs_datetime_after = forms.DateField(
        label='',
        required=False,
        # initial = datetime.datetime.now(),
        widget=forms.DateInput(
            format='yyyy-mm-dd',

            attrs={
                'class': 'form-control',
                'id': 'datepicker2',
                'placeholder': 'published after'
            }))


class QueryDateForm(forms.Form):
    obs_datetime_before = forms.DateField(
        label='',
        required=False,
        # initial = datetime.datetime.now(),

        widget=forms.DateInput(
            format='yyyy-mm-dd',

            attrs={
                'class': 'form-control',
                'id': 'datepicker1',
                'placeholder': 'published before'
            }

        ))

    obs_datetime_after = forms.DateField(
        label='',
        required=False,
        # initial = datetime.datetime.now(),
        widget=forms.DateInput(
            format='yyyy-mm-dd',

            attrs={
                'class': 'form-control',
                'id': 'datepicker2',
                'placeholder': 'published after'
            }))

class QueryAnuallDateForm(forms.Form):
    year_before = forms.IntegerField(
        label='year before',
        required=False,

    )
    year_after = forms.IntegerField(
        label='year after',
        required=False,

    )


class DynamicForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

class metology_infForm(forms.ModelForm):
    survey_date = forms.DateField(
        label='survey_date',
        required=False,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickermetology_survay_date',
                'placeholder': ' '
            }
        )

    )
    open_date = forms.DateField(
        label='open_date',
        required=False,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickermetology_open_date',
                'placeholder': ' '
            }
        )

    )
    close_date = forms.DateField(
        label='close_date',
        required=False,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickermetology_close_date',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = Metology_inf
        fields = ('surveyer_name','survey_date','gps_number','elevation','open_date','close_date','present_condition','obs_item',
                  'meas_frequency','meas_type','condition_of_station','improvement_point')

class MetologyForm(DynamicForm, forms.ModelForm):

    class Meta:
        model = XY_Metology
        fields = (
        'id_field', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
        'sub_baisn', 'image','geom')
        widgets = {'geom': LeafletWidget()}



class humedity_dailyForm(forms.ModelForm):

    obs_date = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            # format='yyyy-mm-dd',
             attrs={
                'class': 'form-control',
                'id': 'datepickerhd',
                'placeholder': ''
            }

        ))
    class Meta:
        model = humidity_daily
        fields = ('obs_date','daily_avg','daily_max','daily_min','max_time','min_time','meas_method','data_source','other_source','remarks')

class humedity_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            # format='yyyy-mm-dd',
            attrs={
                'class': 'form-control',
                'id': 'datepickerhm',
                'placeholder': ''
            }

        ))
    class Meta:
        model = humidity_monthly
        fields = ('obs_datetime','monthly_avg','monthly_max','monthly_min','meas_method','avg_hum_from_daily','remarks')
        # fields = '__all__'
class airpressureForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            # format='yyyy-mm-dd',
            attrs={
                'class': 'form-control',
                'id': 'datepickerair',
                'placeholder': ''
            }

        ))
    class Meta:
        model = airpressure
        # fields = '__all__'
        fields = ('obs_datetime','daily_avg','daily_max','daily_min','meas_method','data_source','other_source','remarks')
    # def __init__(self,*args,**kwargs):
    #         super(airpressureForm,self).__init__(*args,**kwargs)
    #         self.fields['created_by'].empty_label = "select"

class temperature_dailyForm(forms.ModelForm):
    obs_date = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            # format='yyyy-mm-dd',
            attrs={
                'class': 'form-control',
                'id': 'datepickertd',
                'placeholder': ''
            }

        ))
    class Meta:
        model = temperature_daily
        fields = ('obs_date','daily_avg','daily_max','daily_min','max_time','min_time','meas_method','data_source','other_source','remarks')
        # fields='__all__'
    # def __init__(self,*args,**kwargs):
    #     super(temperature_dailyForm,self).__init__(*args,**kwargs)
    #     self.fields['waterpoint'].empty_label = "select"

class temperature_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickertm',
                'placeholder': ''
            }

        ))
    class Meta:
        model = temperature_monthly
        fields = ('obs_datetime','monthly_avg','monthly_max','monthly_min','meas_method','data_source','avg_temp_from_daily','remarks')
class wind_dailyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerwd',
                'placeholder': ''
            }

        ))
    class Meta:
        model = wind_daily
        fields = ('obs_datetime','daily_avg','daily_max','daily_min','meas_method','data_source','other_source','remarks')

class wind_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,

        widget=forms.DateInput(

        # format='yyyy-mm-dd',
            attrs={
                'class': 'form-control',
                'id': 'datepickerwm',
                'placeholder': ''
            }

        ))

    class Meta:
        model = wind_monthly
        fields = ('obs_datetime','avg_monthly_wind_from_hour','remarks')
        # fields = '__all__'

class sunshine_dailyForm(forms.ModelForm):
    obs_date = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            # format='yyyy-mm-dd',
            attrs={
                'class': 'form-control',
                'id': 'datepickersd',
                'placeholder': ''
            }

        ))

    class Meta:
        model = sunshine_daily
        fields = ('obs_date','rad_mj_m2','rad_max_w_m2','max_time','duration_hr','meas_method','data_source','rad_avg_w_m2','other_source','rad_min_w_m2','remarks')

        # fields = '__all__'

class evaporation_dailyForm(forms.ModelForm):
    obs_date = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            # format='yyyy-mm-dd',
            attrs={
                'class': 'form-control',
                'id': 'datepickered',
                'placeholder': ''
            }

        ))
    class Meta:
        model = evaporation_daily
        fields = ('obs_date','evap_mm','meas_method','data_source','other_source','remarks')
    # def __init__(self,*args,**kwargs):
    #         super(evaporation_dailyForm,self).__init__(*args,**kwargs)
    #         self.fields['created_by'].empty_label = "select"

class evaporation_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,

        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerem',
                'placeholder': ''
            }

        ))
    class Meta:
        model = evaporation_monthly
        fields = ('obs_datetime','monthly_avg','meas_method','data_source','other_source','remarks')

class precipitation_dailyForm(forms.ModelForm):
    obs_date = forms.DateField(
        label='obs_date',
        required=True,

        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerpd',
                'placeholder': ''
            }

        ))
    class Meta:
        model = precipitation_daily
        fields = ('obs_date','prcp_mm','meas_method','data_source','other_source','remarks')
        # fields='__all__'
class precipitation_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,

        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerpm',
                'placeholder': ''
            }

        ))
    class Meta:
        model = precipitation_monthly
        fields = ('obs_datetime','monthly_precipitaion','meas_method','data_source','other_source','calculated_value','remarks')

class precipitation_annualForm(forms.ModelForm):
    class Meta:
        model = precipitation_annual
        fields = ('year','annual_precipitation','annual_avg_precipitation','remarks')

class snowdepthForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,

        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickersnowdepth',
                'placeholder': ''
            }

        ))

    class Meta:
        model = snowdepth
        fields = ('obs_datetime','dailysnowdepth','meas_method','data_source','other_source','remarks')

class snowfallForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,

        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickersnowfall',
                'placeholder': ''
            }

        ))

    class Meta:
        model = snowfall
        fields = ('obs_datetime','dailysnowfall','meas_method','data_source','other_source','remarks')
