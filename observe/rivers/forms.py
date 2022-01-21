
from django import forms
from observe.rivers.models import riverdischarge_daily,riverdischarge_anual,riverdischarge_monthly,surface_hq,\
    riverflowmeasure,discharge_survey,sectionareasurvey,sectiondata,XY_River,River_inf
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
from leaflet.forms.widgets import LeafletWidget
class XY_RiverForm(forms.ModelForm):
    class Meta:
        model = XY_River
        fields = ('id_field', 'geom')
        widgets = {'geom': LeafletWidget()}

class RiverForm(DynamicForm, forms.ModelForm):
    # lat = forms.FloatField(widget=forms.HiddenInput())
    # lng = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = XY_River
        fields = (
            'id_field', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
            'sub_baisn', 'image', 'geom')
        widgets = {'geom': LeafletWidget()}

class River_infForm(forms.ModelForm):
    survey_date = forms.DateField(
        label='',
        required=False,
        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerriver_survay_date',
                'placeholder': ''
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
                'id': 'datepickerriver_open_date',
                'placeholder': ''
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
                'id': 'datepickerriver_close_date',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = River_inf
        fields = ('surveyer_name','survey_date','gps_number','water_use','open_date','close_date',
                  'channel_condition','measurment_items','labo_qual_analysis_frequency',
                  'type_of_automatic_sensor','station_condition','equipped_with_stuff_gauge',
                  'field_measur_freq_dryseason','field_measur_freq_rainyseason','measure_type_head',
                  'measure_type_quality','statuse_of_station','improvement_point')

class riverdischarge_dailyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
             # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerrdd',
                'placeholder': ''
            }
        )
         # ,input_formats=['%y-%m-%d'],
    )
    class Meta:
        model = riverdischarge_daily
        fields = ('obs_datetime','rc_id','stage_m','discharge_m3_sec','meas_method','data_source','other_source','remarks')
        # fields = '__all__'
    # def __init__(self,*args,**kwargs):
    #     super(riverdischarge_dailyForm,self).__init__(*args,**kwargs)
    #     self.fields['waterpoint'].empty_label = "select"

class riverdischarge_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=False,
        widget=forms.DateInput(
             # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerrdm',
                'placeholder': ' '
            }
        )
    )


    class Meta:
        model = riverdischarge_monthly
        fields = ('obs_datetime', 'monthly_avg_discharge','monthly_total_discharge','meas_method','data_source','other_source', 'remarks')
        # fields = '__all__'

class riverdischarge_anualForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=False,
        widget=forms.DateInput(
            # format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerrda',
                'placeholder': ' '
            }
        )
   )

    class Meta:
        model = riverdischarge_anual
        fields = ('obs_datetime','anual_discharge','remarks')
        # fields = '__all__'

class riverflowmeasureForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=False,
        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerrfm',
                'placeholder': ' '
            }
        ) )

    class Meta:
            model = riverflowmeasure
            # fields = '__all__'
            fields = ('obs_datetime', 'station_area', 'calculated_flow_velocity','section_id', 'avg_flow_velocity','meas_method', 'equipment_spec','data_source',
                  'other_source', 'remarks')

class discharge_surveyForm(forms.ModelForm):
    year = forms.DateField(
        label='Year',
        required=False,
        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerrds',
                'placeholder': 'year'
            }
        ))

    class Meta:
        model = discharge_survey
        fields = ('year', 'type_of_regression', 'data_limit_low','data_limit_up', 'formula')
        # fields = '__all__'

class sectionareasurveyForm(forms.ModelForm):
    datetime = forms.DateField(
        label='obs_date',
        required=False,
        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerrss',
                'placeholder': 'datetime'
            }
        ))

    class Meta:

            model = sectionareasurvey
            fields = ('datetime', 'sas_area', 'sas_surveyer','sas_method', 'data_source','other_source', 'remarks')
            # fields = '__all__'

class sectiondataForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=False,
        # initial = datetime.datetime.now(),

        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepicker7',
                'placeholder': ' '
            }
        ) )
    class Meta:
            model = sectiondata
            fields = ('sec_datetime', 'sec_stano', 'sec_x','sec_y')

class surface_hqForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_date',
        required=False,
        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerrhq',
                'placeholder': ' '
            }
        ) )

    class Meta:
        model = surface_hq
        # fields = '__all__'
        fields = ('obs_datetime','h','q', 'section_width_m', 'section_depth_m', 'section_area_m2','velocity_m_s','meas_method','remarks')