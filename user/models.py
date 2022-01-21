from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class profile(models.Model):
    image = models.ImageField(default='alt.jpg',upload_to='profile_pic')
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return '{} profile'.format(self.user.username)

def create_profile(sender,**kwarg):
    if kwarg['created']:
        user_profile = profile.objects.create(user=kwarg['instance'])

post_save.connect(create_profile,sender=User)