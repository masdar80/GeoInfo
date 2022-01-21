from django import forms
from observe.models import pumping,pumptest_obswell,step_drawdown,continious_dischage,recovery_test,Waterpoint,pumptest_pumpwell
from leaflet.forms.widgets import LeafletWidget

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

class WaterpointForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = Waterpoint
        fields = ('waterfacilitypoint_id','city','gov','type','agency','town','site','village','basin','geom')
        widgets = {'geom': LeafletWidget()}

class pumpingForm(forms.ModelForm):
    pmp_startdatetime = forms.DateField(
        label='pmp_startdatetime',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepicker-pump-1',
                'placeholder': ' '
            }
        ),
    )
    pmp_time = forms.DateField(
        label='pmp_time',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepicker-pump-13',
                'placeholder': ' '
            }
        ),
    )
    pmp_enddatetime = forms.DateField(
        label='pmp_enddatetime',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepicker-pump-12',
                'placeholder': ' '
            }
        ),
    )
    class Meta:
        model = pumping
        fields=('pmp_pumpdepth','pmp_startdatetime','pmp_enddatetime','pmp_time','pmp_discharge','pmp_pumptype',
               'pmp_generatortype','pmp_dischargemethod','pmp_capacitydevice','pmp_manometertype')

class pumptest_obswellForm(forms.ModelForm):
    class Meta:
        model = pumptest_obswell
        fields =('pto_depth','pto_diameter','pto_swl','pto_distance','pto_reflevel')


class pumptest_pumpwellForm(forms.ModelForm):
    pumptest_interval_from = forms.DateField(
        label='pumptest_interval_from',
        required=True,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerpfrom',
                'placeholder': 'pumptest_interval_from'
            }
        )

    )
    pumptest_interval_to = forms.DateField(
        label='pumptest_interval_to',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerpto',
                'placeholder': 'pumptest_interval_from'
            }
        )

    )
    class Meta:
        model = pumptest_pumpwell
        fields =('pumptest_interval_from', 'pumptest_interval_to', 'pumptest_swl', 'pumptest_diameter')

class step_drawdownForm(forms.ModelForm):
    sdd_datetime = forms.DateField(
        label='sdd_datetime',
        required=True,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerstep-dd',
                'placeholder': ' '
            }
        )

    )
    sdd_accumulatetime = forms.DateField(
        label='sdd_accumulatetime',
        required=True,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickeraccumulate',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = step_drawdown
        fields =('sdd_datetime', 'sdd_accumulatetime',  'pumptest_interval_to', 'sdd_discharge',
                 'sdd_waterdepth', 'sdd_drawdown')

class continious_dischageForm(forms.ModelForm):

    cds_date = forms.DateField(
        label='cds_date',
        required=True,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickercds_date',
                'placeholder': ' '
            }
        )

    )

    class Meta:
        model = continious_dischage

        fields = ('cds_date','cds_accumulate','cds_depth','cds_time','cds_drawdown')

class recovery_testForm(forms.ModelForm):
    rct_datetime = forms.DateField(
        label='rct_datetime',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepicker-recovery',
                'placeholder': ' '
            }
        )
    )

    class Meta:
        model = recovery_test
        fields = ('rct_datetime', 'rct_waterdepth', 'rct_drawdown')

