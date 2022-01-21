from observe.springs.models import springdischarge_anual,springdischarge_avg_monthly,\
    springdischarge_avg_anual,springdischarge_daily,springdischarge_monthly,Spring_inf
from django import forms
from observe.springs.models import XY_Spring
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

class QueryDateMonthForm(forms.Form):
    month_before = forms.CharField(
        label='month before',
        required=False,

       )

    month_after = forms.DateField(
        label='month after',
        required=False,
        )

class QueryDateAnnualForm(forms.Form):
    obs_datetime_before = forms.CharField(
        label='year before',
        required=False,

       )

    month_after = forms.DateField(
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

class Spring_infForm(forms.ModelForm):
    survey_date = forms.DateField(
        label='survey_date',
        required=False,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerspring_survay_date',
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
                'id': 'datepickerspring_open_date',
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
                'id': 'datepickerspring_close_date',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = Spring_inf
        fields = ('surveyer_name','survey_date','gps_number','water_use','open_date','close_date',
                  'present_spring_statuse','spring_ownership','measurment_items','labo_qual_analysis_frequency',
                  'type_of_automatic_sensor','equipped_with_stuff_gauge',
                  'field_measur_freq_dryseason','field_measur_freq_rainyseason','measure_type_head',
                  'measure_type_quality','aquifer_litho_code','condition_of_station','improvement_point')


from leaflet.forms.widgets import LeafletWidget

class SpringForm(DynamicForm, forms.ModelForm):

    class Meta:
        model = XY_Spring
        fields = (
        'id_field', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
        'sub_baisn','image', 'geom')
        widgets = {'geom': LeafletWidget()}


class springdischarge_anualForm(forms.ModelForm):
    # obs_datetime = forms.DateField(
    #     label='obs_datetime',
    #     required=True,
    #
    #     widget=forms.DateInput(
    #
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'datepickersdaf',
    #             'placeholder': 'obs_datetime'
    #         }
    #     ))
    class Meta:
        model = springdischarge_anual
        fields = ('obs_datetime','anual_discharge','remarks')
        # fields = '__all__'

class springdischarge_avg_anualForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='',
        required=True,
        widget=forms.DateInput(
            # format='%y%m%d',

            attrs={
                'class': 'form-control',
                'id': 'datepickersdaa',
                'placeholder': 'obs_datetime'
            }
        ))
    class Meta:
        model = springdischarge_avg_anual
        fields = ('obs_datetime','avg_discharge','max_discharge','min_discharge','remarks')
        # fields ='__all__'
class spring_discharge_dailyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_datetime',
        required=True,
        widget=forms.DateInput(
               attrs={
                'class': 'form-control',
                'id': 'datepickersdd',
                'placeholder': ''
            }

        ))
    class Meta:
        model = springdischarge_daily
        fields = ('obs_datetime','stage_m','rc_id','discharge_m3_sec','meas_method','data_source','other_source','remarks')
        # fields = '__all__'
class springdischarge_avg_monthlyForm(forms.ModelForm):
    # month = forms.DateField(
    #     label='month',
    #     required=False,
    #     widget=forms.DateInput(
    #           attrs={
    #             'class': 'form-control',
    #             'id': 'datepickersdam-1',
    #             'placeholder': ''
    #         }
    #
    #     ))
    class Meta:
        model = springdischarge_avg_monthly
        fields = ('month','avg_discharge','max_discharge','min_discharge','remarks')
        # fields = '__all__'

class springdischarge_monthlyForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_datetime',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickersdm',
                'placeholder': 'obs_datetime'
            }

        ))
    class Meta:
        model = springdischarge_monthly
        fields = ('obs_datetime','monthly_avg_discharge','monthly_total','meas_method','data_source','other_source','remarks')
        # fields = '__all__'

