from django.contrib import admin
from demosky.models import UserProfile

# Register your models here.
from demosky.models import Sensors

admin.site.register(Sensors)



admin.site.register(UserProfile)
