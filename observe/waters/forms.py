
from django import forms
from observe.models import waterchemistrysurvey_station,watersampling,biological,othercommon_parameters,\
    toxic_substances,hydrochemical,heavymetals_rareelement,eutrophication2,fieldparameter
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

class waterchemistrysurvey_stationForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = waterchemistrysurvey_station
        fields = ( 'id_pk','english_name', 'arabic_name', 'sourcetype', 'owner', 'mohafaza', 'montika', 'nahia', 'village',
                  'sub_basin', 'geom')
        widgets = {'geom': LeafletWidget()}


class watersamplingForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerwsample',
                'placeholder': ' '
            }
        )

    )
    taste_datetime = forms.DateField(
        label='taste_datetime',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickertaste_datetime',
                'placeholder': ' '
            }
        )

    )
    sample_datetime = forms.DateField(
        label='sample_datetime',
        required=True,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerwsample_datetime',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = watersampling
        fields =('sample_id','date','sample_datetime','taste_datetime','analysis_type','laboratory_name','remarks')




class heavymetals_rareelementForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerheavymetals_rareelement',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = heavymetals_rareelement
        # fields = '__all__'
        fields =('date', 'Cd', 'Pb', 'Cu', 'Cr', 'Ni', 'Mn', 'Fe', 'Al', 'Zn', 'AS', 'Be', 'cn', 'Li', 'Hg', 'Mo', 'Se', 'Ba', 'Ag', 'units', 'remarks')



class fieldparameterForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerfieldp',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = fieldparameter
        fields = ('date', 'temperature_c', 'do_mg_l', 'ph', 'do_per_cent', 'cond_ms_cm', 'turbidity_ntu', 'smell', 'color', 'taste', 'flow_rate', 'redox')


class eutrophication2Form(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            # format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickereutrophication2',
                'placeholder': ' '
            }
        )

    )

    class Meta:
        model = eutrophication2
        fields=('date','bod_mg_l','do_mg_l','ss','ph','ec','alkalinity','nh3_mg_l','nh4_mg_l','po4','oil','t_n','t_p','toc','si','h2s','remarks')

class hydrochemicalForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerhydrochemical',
                'placeholder': ' '
            }
        )

    )

    class Meta:
        model = hydrochemical
        fields = ('date', 'hard_total_mg_l', 'hard_lime_mg_l', 'hard_mag_mg_l', 'tds_mg_l', 'ca_mg_l', 'mg_mg_l', 'na_mg_l', 'k_mg_l', 'so4_mg_l',
         'free_cl_mg_l', 'cl_mg_l', 'hco3_mg_l', 'co3_mg_l', 'o18_mg_l', 'o18_mg_l', 'h2_mg_l', 'he_mg_l', 'h3_mg_l', 'c14_mg_l', 'ra_mg_l', 'estemated_waterage')



class toxic_substancesForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickertoxic_substances',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = toxic_substances
        fields = ('date','phenol','benzen','mbas','b','f','bhc_a','bhc_b','abs','aox','pcb','dioxin','chlorodan_a')


class othercommon_parametersForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'datepickerothercommon_parameters',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = othercommon_parameters
        fields =('date', 'tss_mg_l', 'p_mg_l', 's_mg_l', 'u_mg_l', 'sr_mg_l', 'co_mg_l')



class biologicalForm(forms.ModelForm):
    date = forms.DateField(
        label='date',
        required=True,
        widget=forms.DateInput(
            format='%y-%m-%d',
            attrs={
                'class': 'form-control',
                'id': 'datepickerbiological',
                'placeholder': ' '
            }
        )

    )
    class Meta:
        model = biological
        fields =('date','coliform_t7a_100ml','sodmons_t7a_100ml','bsodomonas_t7a_24hour','bacteria','ferments_number','helmenth_eggs')

    # def __init__(self, *args, **kwargs):
    #     super(biological, self).__init__(*args, **kwargs)
    #     self.fields['watersampling'].empty_label = "select"

