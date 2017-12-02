from django.contrib import admin
from demosky.models import UserProfile

# Register your models here.
from demosky.models import Sensors

from demosky.models import Chat
from demosky.models import sensormine
from demosky.models import topics
from demosky.models import Sensor_status

admin.site.register(Sensors)




admin.site.register(UserProfile)

admin.site.register(Chat)

admin.site.register(sensormine)

admin.site.register(topics)
admin.site.register(Sensor_status)