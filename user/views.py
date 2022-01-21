from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserCreationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import profile
def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user= form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request,'congradulation {} u  have registered successfully'.format(new_user))
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request,'user/register.html',context)
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'username or password is not correct')
    else:
        form = LoginForm()

    return render(request,'user/login.html',{'form':form,})
def logout_user(request):
    logout(request)
    return render(request,'user/logout.html')
def profile_user(request):

    context={'title':'Your Profile'}
    return render(request,'user/profile.html',context)