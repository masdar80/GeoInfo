from django import forms

# from datetimepicker.widgets import DateTimePicker
# from  .models import riverdischarge_daily,welldischarge_daily,springdischarge_daily

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
                'id': 'datepicker9',
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
                'id': 'datepicker10',
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
                'id': 'datepickerd-1',
                'placeholder': 'published before'
            }

        ))

    obs_datetime_after = forms.DateField(
        label='',
        required=False,
        widget=forms.DateInput(
            format='yyyy-mm-dd',

            attrs={
                'class': 'form-control',
                'id': 'datepickerd-2',
                'placeholder': 'published after'
            }))

