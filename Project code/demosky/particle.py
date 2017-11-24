from django.shortcuts import render, redirect,get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from demosky.forms import RegistrationForm, EditProfileForm, UserProfileForm
from demosky.models import UserProfile
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from random import randint
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
#below headers required for social login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
#for sensors
from demosky.models import Sensors
#from django.http import HttpResponseRedirect, HttpResponse
import json


#sprint 3
from pyowm import OWM
from datetime import datetime,timedelta
import os
from django.templatetags.static import static
import pickle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from itertools import chain

#sprint 4

from .models import Chat
from django.http import JsonResponse
from .models import UserProfile
from django.db import connection
from django.db.models import Q
from newproj import settings


















#######################################
import requests
import json
from sseclient import SSEClient

# r = requests.post('https://api.particle.io/v1/devices/events/chargeState/', data = {'access_token':'2c6c9f8b5229247e2493798a64d8d61052db7428'})
# print (r.content)

messages = SSEClient('https://api.particle.io/v1/devices/events?access_token=2c6c9f8b5229247e2493798a64d8d61052db7428')
i = 0
for msg in messages:
	print i
	print msg
	print type(msg)
	print messages
	i=i+1

	outputMsg = msg.data
	#print outputMsg
	if type(outputMsg) is not str:
		print msg
		#print 'here'
		outputJS = json.loads(outputMsg)
		FilterName = "data"
		event = str(msg.event).encode('utf-8')
		data = str(msg.data).encode('utf-8')
		print event
		print data
		#print( FilterName, outputJS[FilterName] )
		#print outputJS[FilterName]
		#print outputJS
	print "\n"
