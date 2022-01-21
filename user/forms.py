from django.contrib.auth.models import User
from django import forms
# Register your models here.
class UserCreationForm(forms.ModelForm):
    username= forms.CharField(label='User Name')
    email = forms.CharField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name' )
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username' ,'email','first_name','last_name','password','password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!= cd['password2']:
            raise forms.ValidationError('password is not compatible')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username= cd['username']).exists():
            raise forms.ValidationError('username is exists')
        return cd['username']

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='UserName')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password')