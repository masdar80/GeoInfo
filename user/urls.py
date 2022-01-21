from django.contrib import admin
from django.urls import path
from .views import register,login_user,logout_user,profile_user
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from  django.conf import settings

urlpatterns = [
    path('register/', register,name="register"),
    # path('login/', login_user,name="login"),
    # path('logout/', logout_user, name="logout"),
    path('login/', LoginView.as_view(template_name='user/login.html'),name="login"),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    path('profile/', profile_user, name="profile"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
