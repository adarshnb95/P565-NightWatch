from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from django.utils.encoding import python_2_unicode_compatible

class UserProfile(models.Model):
    user= models.OneToOneField(User, unique=True)
    location=models.CharField(max_length=50,default = '')
    birthplace = models.CharField(max_length=50, default='')
    work = models.CharField(max_length=50, default='')
    study = models.CharField(max_length=50, default='')
    photo = models.ImageField(upload_to="profile_image",null=True, blank=True)
    quote=models.TextField(max_length=100,default='')
    bio = models.TextField(max_length=500, default = '')
    token = models.IntegerField(null = True, blank = True)
    fav_sen = models.CharField(max_length=10000, default = '')
    token_valid = models.BooleanField(default = False)


    def __str__(self):
        return self.user.username


def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)



@python_2_unicode_compatible  # only if you need to support Python 2


class Sensors(models.Model):
    sensor_id = models.CharField(max_length=100)
    x_coord = models.FloatField(null=True)
    y_coord = models.FloatField(null=True)
    img_name = models.CharField(max_length=100)
    light_data = models.IntegerField(null=True)
    battery_level = models.FloatField(null=True)
    sensornumber = models.IntegerField(null=True)

    def __str__(self):
        return self.sensor_id
        


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    topic=models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.topic

class topics(models.Model):
    topic=models.CharField(max_length=100)

    def __str__(self):
        return self.topic

class sensormine(models.Model):
    """docstring for ClassName"""
    sensornumber = models.IntegerField(null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    chargestate =  models.FloatField(null=True)
    lightint = models.FloatField(null=True)


    def __int__(self):
        return self.sensornumber
        