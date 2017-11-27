from django.contrib import admin
from demosky.models import UserProfile

# Register your models here.
from demosky.models import Sensors

from demosky.models import Chat
from demosky.models import sensormine

admin.site.register(Sensors)



admin.site.register(UserProfile)

admin.site.register(Chat)

admin.site.register(sensormine)

