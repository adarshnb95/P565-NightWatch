from django.shortcuts import render, redirect,get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from demosky.forms import RegistrationForm, EditProfileForm, UserProfileForm
from demosky.models import UserProfile

from django.contrib import messages,auth
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from random import randint
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required,user_passes_test
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

####################################varun##########################################################



def token_check(user):
    newEmailUser = UserProfile.objects.get(user=user)
    print (newEmailUser.token_valid)
    return newEmailUser.token_valid

## this has to be at the top########
##############################end Varun#########################################################





# Create your views here.
def test():
    pass
    a = Sensors.objects.all()
    bundle = {}
    for j in a:
        bundle[int(j.sensor_id)] = [str(j.sensor_id),j.x_coord,j.y_coord,str(j.img_name),j.light_data,j.battery_level]
    #print bundle
    return bundle


def home1(request):
    full_list = json.dumps(test())
    light_list = json.dumps(ldat())
    weather_data = json.dumps(weathermine())
    return render(request,'demosky/homebasic.html',{'full_list':full_list , 'light_list':light_list , 'weather_data':weather_data })

def terms(request):
    pass
    return render(request,'demosky/termscond.html')



# Create your views here.
@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def home(request):
    testvalue = request.user
    fav_sensors = json.dumps(get_favs(testvalue))
    full_list = json.dumps(test())
    light_list = json.dumps(ldat())
    weather_data = json.dumps(weathermine())
    sensorlist = Sensors.objects.all()
    return render(request,'demosky/home.html',{'full_list':full_list , 'light_list':light_list , 'weather_data':weather_data, 'sensorlist' : sensorlist , 'fav_sensors' : fav_sensors })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/demosky/login/')
        else:
            return render(request, 'demosky/reg_form.html', {'form': form})
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'demosky/reg_form.html', args)

@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def profile(request):
    args = {'user': request.user}
    return render(request, 'demosky/profile.html', args)

@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST , instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            (request.user.userprofile).save()
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/demosky/profile')
    else:
            user_form = EditProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.userprofile)
            args ={'user_form':user_form, 'profile_form': profile_form}
            return render(request,'demosky/edit_profile.html', args)



#------------Varun------------------------------------------


@login_required
def verify(request):
    if request.method == 'POST':
        print (request.POST)
        token = request.POST.get('token')
        forms = request.POST.get('tokenform')       
        newEmailUser = UserProfile.objects.get(user=request.user)
        print (newEmailUser.token)
        print (token)
        if(int(token) == int(newEmailUser.token) ):
            newEmailUser.token_valid = True
            newEmailUser.save()
            return redirect('/demosky/')
        else:
            error = ("Invalid Token.")
            return render(request,'demosky/verify-user.html',{'error' : error}) 
    else:   
        newEmailUser = UserProfile.objects.get(user=request.user)
        newEmailUser.token = randint(10000,99999)
        email = EmailMessage('Token for Login', 'Please use this token for login : '+ str(newEmailUser.token)
            , to=[newEmailUser.user.email])
        email.send()
        newEmailUser.save()
        return render(request, 'demosky/verify-user.html') 




#def handle_uploaded_file(f):
 #   dest = open('/media/profile_image/', 'w')  # write should overwrite the file

  #  for chunk in f.chunks():
   #     dest.write(chunk)
    #dest.close()

       # profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=request.user.userprofile)
       # instance = profile_form.save(commit=False)
       # instance.save()
       # return HttpResponseRedirect("/demosky/edit_profile")

    # return redirect('/demosky/profile')

        # def password_reset(request):
        # 	if request.method == 'POST':
        # 		form = PasswordResetForm(request.POST)
        # 		data = request.POST
        # 		subject = "Thanks  !"
        # 		send_mail(subject,"Hello!!!!!1",'varun.machingal@gmail.com',['varun.machingal@gmail.com'])
        # 		return redirect('/demosky')
        # 	else:
        # 		form =PasswordResetForm()
        # 		args = {'form' : form}
        # 		return render(request, 'demosky/reset-password.html', args)

#def profile_pic(request):
#    if request.method == 'POST':
#        pic_form = ProfilePicForm(request.POST or None, request.FILES, request.user.userprofile)

 #       if pic_form.is_valid():
 #           pic_form.save()
 #           return redirect('/demosky/profile')
 #   else:
 #       pic_form = ProfilePicForm(request.user.userprofile)
 #       args ={'pic_form':pic_form}
 #       return render(request,'demosky/profile_pic.html',args)





 #rahul-------------


 
@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'demosky/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'demosky/password.html', {'form': form})


#################sprint 3 code
def ldat():
    pass
    a = Sensors.objects.all()
    lightdat = {}
    for j in a:
              lightdat[int(j.sensor_id)] = [j.light_data,str(j.sensor_id)]
    #print bundle
    return lightdat




##########Varun##############

@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def manageuser(request):
    if request.method == 'POST':
        print( request.POST)
        userlist = dict(request.POST)['userlist']
        users = User.objects.all()
        if userlist is not None:
            for user in users:
                if str(user.id) not in userlist:
                    user.is_staff = False
                    user.save()
                else:
                    user.is_staff = True
                    user.save()    

            error = "Users changed to admin successfully."
        else:
            
            error = "No User roles changed"

        args = {
                'users': users,
                'error': error
            }    
            
        return render(request,'demosky/manage-user.html', args)   
    else:    
        users = User.objects.all()
        print (users)
        return render(request,'demosky/manage-user.html',{'users':users})            


@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def managesensors(request):
    print(request.POST)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if(action == 'add'):
            xcord = request.POST.get('x-coord')
            print(xcord)
            ycord = request.POST.get('y-coord')
            prev = Sensors.objects.last()
            id = int(prev.sensor_id)+1
            sens = Sensors(sensor_id =str(id),x_coord = xcord, y_coord = ycord)
            sens.save()
            error = "Sensors added successfully."
        elif(action == 'delete'):
            sensorlist = request.POST.get('sensorlist')
        
            if sensorlist is not None:
                for sensor in sensorlist:
                   print(sensor)
                   removeSensor = Sensors.objects.get(sensor_id=str(sensor))
                   removeSensor.delete()
                error = "Sensors deleted successfully."
            else:
                error = "No Sensors deleted"
        else:
            sensorslist = Sensors.objects.all()
            for sensor in sensorslist:
                xcord = request.POST.get(sensor.sensor_id+'_x')
                ycord = request.POST.get(sensor.sensor_id+'_y')
                sensor.x_coord = xcord
                sensor.y_coord = ycord
                sensor.save() 
            error = "Sensors Modified successfully."
        
        sensors = Sensors.objects.all()
        return render(request,'demosky/manage-sensors.html',{'sensors':sensors, 'error' : error})        

    else:
        sensors = Sensors.objects.all()
        return render(request,'demosky/manage-sensors.html',{'sensors':sensors, 'error':""})
#######end-Varun##############



#####rahul###################


def weathermine():

    cond = 1

    try:
        itemlist = pickle.load(open('static/DarkSky-Dev/weather/weather.txt', 'r'))
    except Exception as e:
        cond = 0
        itemlist = ['2017-10-27 07:04:55+160000']

    
    date_tomorrow = datetime.today().date() + timedelta(days=1)

    test_var = datetime.strptime(itemlist[0], "%Y-%m-%d %H:%M:%S+%f")

    # need to run this logic with adarsh , varun , shantanu
    if ((cond ==0) or (test_var.date()>=date_tomorrow)):
        #print itemlist
        print("dates behind clearing")
        open('static/DarkSky-Dev/weather/weather.txt',"w").close()
    

        API_key =  '9a372f943ba48f409d680757e551c422'

        owm = OWM(API_key)
        
        fc = owm.three_hours_forecast('shoals,us')

        f = fc.get_forecast() 

        lst = f.get_weathers()

        b = []
        itemlist=[]

        for weather in f:
            #print (weather.get_reference_time('iso'),weather.get_status(),weather.get_detailed_status(),weather.get_temperature('celsius'))
            a = weather.get_temperature('celsius')

            b.append(weather.get_reference_time('iso'))
            b.append(weather.get_status())
            b.append(weather.get_detailed_status())
            b.append(a['temp'])

            out = open('static/DarkSky-Dev/weather/weather.txt', 'wb')
            pickle.dump(b, out)
            out.close() # close it to make sure it's all been written
            itemlist = b
    return itemlist


def favourites_mark(request):
    pass
    # data = { 'value': 'pass' }
    # return JsonResponse(data);

    if request.method == 'POST':
        pass
        post_text = request.POST.get('uname')
        post_uname = request.POST.get('uname')
        post_sen = request.POST.get('var1')
        a = UserProfile.objects.filter(user__username=post_uname)

        for x in a:
            z = x.fav_sen.split(",")
            print(z)
            print(type(z[0]))
            if post_sen in z:
                print("its present skipping")
                z.remove(post_sen)
                print
                z
                x.fav_sen = ''
                for k in z:
                    x.fav_sen = x.fav_sen + k + ','
                x.save()
                data = {'value': 'pass'}
                return JsonResponse(data);
            x.fav_sen = x.fav_sen + post_sen + ','
            # print x.fav_sen
            x.save()

        data = {'value': 'pass'}
        return JsonResponse(data);
    else:
        data = {'value': 'fail'}
        return JsonResponse(data);


def get_favs(name):
    pass
    uname = name
    retval = []
    a = UserProfile.objects.filter(user__username=uname)
    for x in a:
        z = x.fav_sen.split(",")
        retval = z
    return retval
##################################end rahul###################################################

##################################Varun#######################################################


def logout(request):
    newEmailUser = UserProfile.objects.get(user=request.user)
    newEmailUser.token_valid = False
    newEmailUser.save()
    auth.logout(request)
    return redirect('/demosky/login')


##############################end varun##############################################################

#####################################Shantanu##################################################


@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'demosky/profile.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST , instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            (request.user.userprofile).save()
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/demosky/profile')
    else:
            user_form = EditProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.userprofile)
            args ={'user_form':user_form, 'profile_form': profile_form}
            return render(request,'demosky/edit_profile.html', args)

@login_required
def search(request):
    print(request.POST)
    if request.method == 'POST':
        action = request.POST.get('action')

        if (action == 'uname'):
            key1 = request.POST.get('u-name')
            print(key1)
            if key1:
                if User.objects.filter(username=key1).exists():
                    u = User.objects.get(username=(key1))
                    args = {'user': u}
                    return render(request, 'demosky/search_profile.html', args)
                else:

                    SearchUser = User.objects.filter(
                        Q(username__icontains=key1) |
                        Q(first_name__icontains=key1) |
                        Q(last_name__icontains=key1)
                    )
                    searchlist = list(SearchUser)

                    if searchlist:
                        return render(request, 'demosky/search.html', {'error1': searchlist})
                    else:
                        error = "No such User exists!"
                        return render(request, 'demosky/search.html', {'error': error})
            else:
                error = 'Please enter a search key!'
                return render(request, 'demosky/search.html', {'error': error})

        if (action == 'keysearch'):
            print('reached here')
            username = request.POST.get('result')
            print(username)
            if User.objects.filter(username=username).exists():
                print(username)
                u = User.objects.get(username=(username))
                args = {'user': u}
                return render(request, 'demosky/search_profile.html', args)
            else:
                error = "Try entering a search key first!"
                return render(request,'demosky/search.html',{'error' : error})

        if (action == 'key'):
            key = request.POST.get('key')
            print(key)
            if key:
                if User.objects.filter(username=key).exists():
                    u = User.objects.get(username=(key))
                    args = {'user': u}
                    return render(request, 'demosky/search_profile.html', args)
                else:
                    SearchProfile = UserProfile.objects.filter(
                        Q(bio__icontains=key) |
                        Q(location__icontains=key) |
                        Q(quote__icontains=key) |
                        Q(birthplace__icontains=key) |
                        Q(work__icontains=key) |
                        Q(study__icontains=key)|
                        Q(fav_sen__icontains=key)

                )

#                   SearchUser = User.objects.filter(
#                        Q(username__icontains=key)|
#                        Q(first_name__icontains=key)|
#                        Q(last_name__icontains=key))
#                        print(SearchProfile)
#                        print(SearchUser)
#                        print(search)
#                    searchlist=list(set(search))
#                    print(searchlist)
#               for obj in searchlist:
#                   username = obj.user;
#                   print(username)
#                   error = username
                    searchlist = list(SearchProfile)
                    if searchlist:
                        return render(request, 'demosky/search.html', {'error1': searchlist})
                    else:
                        pass
            else:
                error = 'Please enter a search key!'
                return render(request, 'demosky/search.html', {'error': error})
        else:
            pass


    return render(request, 'demosky/search.html')

@login_required
def Chatbox(request):
    c = Chat.objects.all()
    return render(request, "demosky/chat_box.html", {'home': 'active', 'chat': c})

@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        print(msg)
        c = Chat(user=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
def Messages(request):
    c = Chat.objects.all()
    return render(request, 'demosky/messages.html', {'chat': c})



##################################### end Shantanu##################################################