from observe.wells.models import groundwaterlevel,groundwaterlevel_manual,auto_groundwater,wells_quality,\
    welltoplevel,welllogging,lithologging,loggingdata,log_plot,drilling,casing,packing,well_inf
from django import forms


# from datetimepicker.widgets import DateTimePicker
# from  .models import riverdischarge_daily,welldischarge_daily,springdischarge_daily
from observe.wells.models import XY_Well
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

class WellForm(DynamicForm, forms.ModelForm):

    class Meta:

        model = XY_Well
        fields = (
        'id_field', 'sitename_a', 'sitename_e', 'type', 'agency', 'mohafaza', 'montika', 'nahia', 'village',
        'sub_baisn','image','geom')
        widgets = {'geom': LeafletWidget()}


class groundwaterlevelForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_datetime',
        required=False,
        # initial = datetime.datetime.now(),

        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickergwl',
                'placeholder': ''
            }
        ))
    class Meta:
        model = groundwaterlevel
        # fields = '__all__'
        fields = ('obs_datetime','depth_to_water','waterlevel','meas_method','data_source','other_source','remarks')

class groundwaterlevel_manualForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_datetime',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickergwlm',
                'placeholder': ''
            }
        ))
    class Meta:
        model = groundwaterlevel_manual
        # fields = '__all__'
        fields = ('obs_datetime','depth_to_water','waterlevel','meas_method','data_source','other_source','remarks')
class auto_groundwaterForm(forms.ModelForm):
    obs_date = forms.DateField(
        label='obs_date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickeragw',
                'placeholder': ''
            }
        ))
    class Meta:
        model = auto_groundwater
        # fields = '__all__'
        fields = ('obs_date','depth_m','gw_level_m')
class wells_qualityForm(forms.ModelForm):
    obs_datetime = forms.DateField(
        label='obs_datetime',
        required=True,
        # initial = datetime.datetime.now(),

        widget=forms.DateInput(

            attrs={
                'class': 'form-control',
                'id': 'datepickerwq',
                'placeholder': ''
            }

        ))
    class Meta:
        model = wells_quality
        # fields = '__all__'
        fields = ('obs_datetime','ph','ec_ms_m','temp','meas_method','data_source','other_source','remarks')


class welltoplevelForm(forms.ModelForm):
    meas_date = forms.DateField(
        label='meas_date',
        required=True,

        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerwtl',
                'placeholder': ''
            }
        ))
    class Meta:
        model = welltoplevel
        # fields = '__all__'
        fields = ('meas_date','x_stm','y_stm','z_stm','x_utm','y_utm','z_utm','ground_level','top_concrete','top_casing','source','method','accuracy','convert_g_sys')


class wellloggingForm(forms.ModelForm):
    log_from = forms.DateField(
        label='log_from',
        required=False,
        # initial = datetime.datetime.now(),
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerwl',
                'placeholder': 'log_from'
            }
        ))
    log_to = forms.DateField(
        label='log_to',
        required=False,
        # initial = datetime.datetime.now(),
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerwl-1',
                'placeholder': 'log_to'
            }
        ))
    class Meta:
        model = welllogging
        fields = ('log_from','log_to','log_layer','log_type','data_source','other_source','revision_inf')

class lithologgingForm(forms.ModelForm):
    depth_from = forms.DateField(
        label='depth_from',
        required=True,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerll',
                'placeholder': 'depth_from'
            }
        ))
    depth_to = forms.DateField(
        label='depth_to',
        required=True,
        widget=forms.DateInput(
            format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerll-1',
                'placeholder': 'depth_from'
            }
        ))
    class Meta:
        model = lithologging

        # fields = '__all__'
        fields = ('depth_from','depth_to','description','rock','code','age1','age2','age3','hydrocondition','hydromedia',
        'aquifertype','sgwl','data_source','other_source','revision_inf')
class loggingdataForm(forms.ModelForm):
    class Meta:
        model = loggingdata
        # fields = '__all__'
        fields = ('logdata_type','depth','value','data_source','other_source','remarks')

class log_plotForm(forms.ModelForm):
    class Meta:
        model = log_plot
        # fields = '__all__'
        fields = ('old_id','log_design','log_description','log_inf')

class drillingForm(forms.ModelForm):
    drilling_from = forms.DateField(
        label='drilling_from',
        required=True,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerdrill',
                'placeholder': 'drilling_from'
            }
        ))
    drilling_to = forms.DateField(
        label='drilling_to',
        required=False,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerdrill-1',
                'placeholder': 'drilling_to'
            }
        ))
    class Meta:

        model = drilling
        # fields = '__all__'

        # class Meta:
        #     exclude = ('waterpoint',)
        fields = ('drilling_from','drilling_to','drilling_diameter','drilling_layer','data_source','other_source','remarks')

class casingForm(forms.ModelForm):
    casing_from = forms.DateField(
        label='casing_from',
        required=True,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickercasing',
                'placeholder': 'casing_from'
            }
        ))
    casing_to = forms.DateField(
        label='casing_from',
        required=False,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickercasing-1',
                'placeholder': 'casing_to'
            }
        ))

    class Meta:
        model = casing
        # fields = '__all__'
        fields = ('casing_from','casing_to','casing_diameter','casing_type','data_source','other_source','remarks')
class packingForm(forms.ModelForm):
    packing_from = forms.DateField(
        label='packing_from',
        required=True,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerpacking',
                'placeholder': 'packing_from'
            }
        ))
    packing_to = forms.DateField(
        label='packing_to',
        required=False,
        widget=forms.DateInput(
            # format='%y%m%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerpacking-1',
                'placeholder': 'packing_from'
            }
        ))

    class Meta:
        model = packing
        # fields = '__all__'
        fields = ('packing_from','packing_to','packing_layer')

class Well_infForm(forms.ModelForm):
    survey_date = forms.DateField(
        label='survey_date',
        required=False,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerwell_survay_date',
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
                'id': 'datepickerwell_open_date',
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
                'id': 'datepickerwell_close_date',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = well_inf
        fields = ('surveyer_name', 'survey_date', 'gps_number', 'well_completion_date',
                  'open_date', 'close_date',
                  'water_use', 'atitude_of_top_of_well', 'total_depth', 'well_ownership',
                  'well_oner_name', 'dia_top_casing',
                  'min_dia_casing', 'pump_installed_in_the_well', 'measurment_items',
                  'gw_meas_freq_dryseason', 'gw_meas_freq_dryseason', 'gw_meas_freq_rainyseason',
                  'labo_qual_analysis_freq_drysea',
                 'labo_qual_analysis_freq_rainysea','type_of_measurment','type_of_automatic_sensor','sensor_depth',
                 'condition_of_station','improvement_point' )


