import requests
import json
from sseclient import SSEClient
import datetime

import sys
sys.path.append('D:\IUB\SE\P565-NightWatch\Project code')

import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'newproj.settings'
application = get_wsgi_application()

from demosky.models import sensormine
from demosky.models import Sensor_status

messages = SSEClient('https://api.particle.io/v1/devices/events?access_token=ba90ecc470ec092cdb694c67897b6335a2191c61')

i=0
j=0
pulse_val = 0.0
charge_state = 0.0
for msg in messages:
	i=i+1
	outputMsg = msg.data
	print i
	print msg
	print outputMsg
	
	if type(outputMsg) is not str:
		outputJS = json.loads(outputMsg)
		FilterName = "data"
		FilterName1 = "coreid"
		event = str(msg.event).encode('utf-8')
		data = str(msg.data).encode('utf-8')
		print event
		print "\n"
		data1 = msg.data
		if event == 'pulse' or event == 'currentTime' or event == 'chargeState':
			pass
			if event == 'pulse':
				pass
				pulse_val = outputJS[FilterName]
				j=j+1
			if event == 'currentTime':
				pass
				j=j+1				
			if event == 'chargeState':
				pass
				charge_state = outputJS[FilterName]
				j=j+1
			if j==3:
				pass
				j=0
				idnum = int(int(outputJS[FilterName1])/10000000000000000000)
				test = sensormine(chargestate = charge_state , lightint = pulse_val , sensornumber = idnum , date = datetime.date.today() , dateandtime = datetime.datetime.now() )
				test.save()
				senlist = []
				sensors = Sensor_status.objects.all()
				for x in sensors:
					pass
					senlist.append(int(x.sensor_id))
					print senlist
				if idnum in senlist:
					pass
					t = Sensor_status.objects.get(sensor_id = idnum)
					t.status = True
					t.save()
				else:
					pass
					test1 = Sensor_status(sensor_id = idnum , status = True)
					test1.save()
			
			
			