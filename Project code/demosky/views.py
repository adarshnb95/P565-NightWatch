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

#sprint 5
from .models import topics
from demosky.models import sensormine
from demosky.models import Sensor_status
from django.db.models import Max


####################################varun##########################################################



def token_check(user):
    newEmailUser = UserProfile.objects.get(user=user)
    print (newEmailUser.token_valid)
    return newEmailUser.token_valid

## this has to be at the top########
##############################end Varun#########################################################

#return a list of sensors that need to be promoted
def get_unpromoted_sensors():
    pass
    #get all the sensor objects
    a = Sensors.objects.all()
    #initialize empty dictionary
    bundle = []
    # iterate through the objects
    for j in a:
        #check if the sensor is active
        if (j.status):
            #check if it needs to be promoted
            if (j.add_admin):
                pass
            else:
                #put the value in the list
                bundle.append(int(j.sensor_id))
                bundle.append(str(j.sensor_id))
                bundle.append(j.sensornumber)
    #print bundle
    return bundle   



# Create your views here.
#this function returns a list of active AND added sensors
def test():
    pass
    #get all the sensor objects
    a = Sensors.objects.all()
    #initialize empty dictionary
    bundle = {}
    # iterate through the objects
    for j in a:
        #check if the sensor is active AND added
        if (j.status) and (j.add_admin):
            #add to the dictionary 
            bundle[int(j.sensor_id)] = [str(j.sensor_id),j.x_coord,j.y_coord,str(j.img_name),j.light_data,j.battery_level,j.status,j.add_admin ]
    #print bundle
    return bundle

#this is for the default landing page
def home1(request):
    update_data()
    #obtain list of valid sensors
    full_list = json.dumps(test())
    #obtain list of sensors and their light intensity
    light_list = json.dumps(ldat())
    #obtain weather data
    weather_data = json.dumps(weathermine())
    #render the data
    return render(request,'demosky/homebasic.html',{'full_list':full_list , 'light_list':light_list , 'weather_data':weather_data })

def terms(request):
    pass
    return render(request,'demosky/termscond.html')



# Create your views here.
@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def home(request):
    update_data()
    #create_csv()
    #obtain the sensor data for chart plotting for the current day
    chart_data_day = json.dumps(chartmine_day())
    #obtain data for chart plotting over 12 months
    chart_data = json.dumps(chartmine())
    #get the current user
    testvalue = request.user
    #obtain a list of sensors the user has marked as his favourites
    fav_sensors = json.dumps(get_favs(testvalue))
    #obtain list of valid sensors
    full_list = json.dumps(test())
    #obtain list of sensors and their light intensity
    light_list = json.dumps(ldat())
    #obtain weather data
    weather_data = json.dumps(weathermine())
    #obtain all of the sensor objects
    sensorlist = Sensors.objects.all()
    #pass data to the page to be rendered
    return render(request,'demosky/home.html',{'full_list':full_list , 'light_list':light_list , 'weather_data':weather_data, 'sensorlist' : sensorlist , 'fav_sensors' : fav_sensors , 'chart_data' : chart_data , 'chart_data_day' : chart_data_day })


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

#obtain light intensity data
def ldat():
    pass
    #obtain all of the sensor objects
    a = Sensors.objects.all()
    #initialize light intensity dictionary
    lightdat = {}
    #iterate over the objects
    for j in a:
        #check if the sensor is valid and active
        if (j.status) and (j.add_admin):
            lightdat[int(j.sensor_id)] = [j.light_data,str(j.sensor_id)]
    #print bundle
    #return light intensity
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
    #get list of sensors that need to be managed the return is of teh form [ sensor id(int) , sensor id (str) , sensornumer(int)]
    unpromoted_sensors = get_unpromoted_sensors()[::3]
    print(unpromoted_sensors)
    print(request.POST)
    if request.method == 'POST':
        action = request.POST.get('action')

        if(action == 'add'):

            for uns in unpromoted_sensors:
                if str(uns)+'_x1' in request.POST:
                    x1= request.POST.get(str(uns)+'_x1')
                    y1 = request.POST.get(str(uns)+'_y1')
                    if(x1 is not '' and y1 is not '' ):
                        print("x---"+str(x1))
                        sen = Sensors.objects.get(sensor_id =uns)
                        sen.x_coord = x1
                        sen.y_coord = y1
                        sen.add_admin = True
                        sen.save()
                        unpromoted_sensors = get_unpromoted_sensors()[::3]
            error = "Sensors added successfully."
        elif(action == 'delete'):
            sensorlist = dict(request.POST)['sensorlist'] 

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
        return render(request,'demosky/manage-sensors.html',{'sensors':sensors, 'unpromotedsensors': unpromoted_sensors, 'error' : error})

    else:
        sensors = Sensors.objects.all()
        return render(request,'demosky/manage-sensors.html',{'sensors':sensors, 'unpromotedsensors': unpromoted_sensors, 'error':""})
#######end-Varun##############



#####rahul###################

#obtain weather data
def weathermine():

    cond = 1
    #attempt to open the file which gets created after the first run
    try:
        #open the file , the file is stored as a pickle
        itemlist = pickle.load(open('static/DarkSky-Dev/weather/weather.txt', 'r'))
    except Exception as e:
        #file hasnt been found and we set a list to contain an old date
        cond = 0
        itemlist = ['2017-10-27 07:04:55+160000']

    #get tomorrows date


    date_tomorrow = datetime.today().date() + timedelta(days=1)
    #get the oldest date from the file
    test_var = datetime.strptime(itemlist[0], "%Y-%m-%d %H:%M:%S+%f")

    # need to run this logic with adarsh , varun , shantanu
    # check if the date pulled from the file is the same as tomorrows date if it is that means we need to call the api and get latest data
    if ((cond ==0) or (test_var.date()>=date_tomorrow)):
        #print itemlist
        #print("dates behind clearing")

        #create a new file
        open('static/DarkSky-Dev/weather/weather.txt',"w").close()


        API_key =  '9a372f943ba48f409d680757e551c422'
        #call the api
        owm = OWM(API_key)
        #get forecast of a location
        fc = owm.three_hours_forecast('shoals,us')

        f = fc.get_forecast()
        #get weather from the forecast
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
                print(z)
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







#update data
def update_data():
    pass
    #get all sensors
    sensors = Sensor_status.objects.all()
    #print sensors
    #create empty sensor list
    sensorlist = []
    #specify the date format
    date_format = "%Y-%m-%d"


    max_val = Sensors.objects.all().aggregate(Max('sensor_id'))
    #print max_val
    latest_vale=0

    for key, value in max_val.items():
        latest_vale = int(value)

    # print latest_vale
    # print type(latest_vale)
    for i in sensors:
        #print i.status
        sensorlist.append(int(i.sensor_id))

    sensormine_data = sensormine.objects.all()

    #print sensormine_data
    # for i in sensormine_data:
    #     print i.sensornumber

    for j in sensorlist:
        sensormine_data = sensormine.objects.filter(sensornumber=j).order_by('-dateandtime')

        for m in sensormine_data:

            active = False

            #print (m.sensornumber,m.dateandtime,m.chargestate)

            #now have the latest data of a particular sensor
            #determine if it is active - see if the difference in date is 1 day


            data_date = str(m.dateandtime.date())
            todays_data = str(datetime.today().date())
            a = datetime.strptime(todays_data, date_format)
            b = datetime.strptime(data_date, date_format)
            delta = a - b
            #print delta.days

            if (delta.days>=2):
                pass
                #it means the senor data is two day old at least and not active
            else:
                #itmeans the sensor is active
                active = True

            #we have now established the sensor is active
            #now we need to either create a new entry in the sensor table or update an existing one

            try:
                pass
                testvariable = Sensors.objects.get(sensornumber= m.sensornumber)
                #found a matching entry all we need to do is update
                testvariable.light_data = m.lightint
                testvariable.battery_level = m.chargestate
                testvariable.status = active
                testvariable.save()


            except Exception as e:
                pass
                #no matching entry found and thus we need to create the entry
                latest_vale = latest_vale+1
                newsensor = Sensors(sensor_id = str(latest_vale),light_data = m.lightint , battery_level = m.chargestate , sensornumber = m.sensornumber , status = active , add_admin = False)
                newsensor.save()

            break

       # print ("nextloop")



#create a csv file
def create_csv(name):
    pass
    name_1 = name 
    #create a csv file
    location_1 = 'static/DarkSky-Dev/csv/'+ str(name)+'.csv'
    outF = open(location_1, "w")


    sensors = Sensor_status.objects.all()
    #print sensors
    sensorlist = []
    #obtain list of sensors
    for i in sensors:
        #print i.status
        sensorlist.append(int(i.sensor_id))

    sensormine_data = sensormine.objects.all()
    #for each sensor store data
    for j in sensorlist:
        sensormine_data = sensormine.objects.filter(sensornumber=j).order_by('-dateandtime')

        for m in sensormine_data:

            #print m.sensornumber,m.dateandtime,m.chargestate
            line = ''
            line = str(m.sensornumber)+","+str(m.dateandtime)+","+str(m.chargestate)+","+str(m.lightint)+"\n"
            outF.write(line)
    outF.close()



def download_csv(request):
    pass
    # data = { 'value': 'pass' }
    # return JsonResponse(data);
    username_1 = request.user
    location_2 = 'static/DarkSky-Dev/csv/'+ str(username_1)+'.csv'
    
    newEmailUser_1 = UserProfile.objects.get(user=request.user)
    create_csv(username_1)


    newEmailUser = UserProfile.objects.get(user=request.user)
    newEmailUser.token = randint(10000,99999)
    email = EmailMessage('Nightswatch CSV download', 'Please find attached the CSV file you requested'
            , to=[newEmailUser.user.email])
    email.attach_file(location_2)
    email.send()

    data = {'value': 'pass'}
    return JsonResponse(data);


    # if request.method == 'POST':
    #     pass
    #     post_text = request.POST.get('uname')
    #     post_uname = request.POST.get('uname')
    #     post_sen = request.POST.get('var1')
    #     a = UserProfile.objects.filter(user__username=post_uname)

    #     for x in a:
    #         z = x.fav_sen.split(",")
    #         print(z)
    #         print(type(z[0]))
    #         if post_sen in z:
    #             print("its present skipping")
    #             z.remove(post_sen)
    #             print(z)
    #             x.fav_sen = ''
    #             for k in z:
    #                 x.fav_sen = x.fav_sen + k + ','
    #             x.save()
    #             data = {'value': 'pass'}
    #             return JsonResponse(data);
    #         x.fav_sen = x.fav_sen + post_sen + ','
    #         # print x.fav_sen
    #         x.save()

    #     data = {'value': 'pass'}
    #     return JsonResponse(data);
    # else:
    #     data = {'value': 'fail'}
    #     return JsonResponse(data);







def chartmine():
    pass
    #create a dictionary which has sensor number for keys and as values a list of list [[jan],[feb] ........[dec]]
    temp_dict = {}

    #get the sensors data
    sensorlist = []
    sensors = Sensor_status.objects.all()
    for i in sensors:
        #print i.status
        sensorlist.append(int(i.sensor_id))

    sensormine_data = sensormine.objects.all()

    #initialize dict

    for n in sensorlist:
        temp_dict[str(n)] = [[],[],[],[],[],[],[],[],[],[],[],[]]


    # print (temp_dict)


    for j in sensorlist:
        sensormine_data = sensormine.objects.filter(sensornumber=j).order_by('date')


        for m in sensormine_data:
            #now for each sensor we have arranged in increasing order of date
            date_temp = str(m.date)
            temp1 = date_temp.split('-')
            month_temp = temp1[1]

            temp_dict[str(m.sensornumber)][int(month_temp)-1].append(m.lightint)

    #         print (date_temp.split('-') , month_temp  , m.sensornumber , m.lightint)
    # print (temp_dict)

    #now need to put the data in a proper data structure 
    returnlist = []
    for key in temp_dict:
        returnlist.append(int(key))
        c = temp_dict[key]
        #print c
        for s in range(0,12):
            denom = 1
            if (len(c[s])> 0):
                denom = len(c[s])
            list_value_temp = sum(c[s])/ denom
            returnlist.append(list_value_temp)
    # print ("returnlist")
    # print (returnlist)
    # print ("^returnlist")
    return returnlist


def chartmine_day():
    pass
    #create a dictionary which has sensor number for keys and as values a list of list [[jan],[feb] ........[dec]]
    temp_dict = {}

    #get the sensors data
    sensorlist = []
    sensors = Sensor_status.objects.all()
    for i in sensors:
        #print i.status
        sensorlist.append(int(i.sensor_id))

    sensormine_data = sensormine.objects.all()

    #initialize dict

    for n in sensorlist:
        temp_dict[str(n)] = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]


    print (temp_dict)


    for j in sensorlist:
        sensormine_data = sensormine.objects.filter(sensornumber=j).filter(date=datetime.today().date()).order_by('time')


        for m in sensormine_data:
            #now for each sensor we have arranged in increasing order of time
            print (m.dateandtime,m.time,m.sensornumber)


            time_temp = str(m.time)
            temp2 = time_temp.split(':')
            time1_temp = temp2[0]

            temp_dict[str(m.sensornumber)][int(time1_temp)].append(m.lightint)

            #print (date_temp.split('-') , month_temp  , m.sensornumber , m.lightint)
            #print "^for loop"
    print (temp_dict)

    # #now need to put the data in a proper data structure 
    returnlist = []
    for key in temp_dict:
        returnlist.append(int(key))
        c = temp_dict[key]
        #print c
        for s in range(0,24):
            denom = 1
            if (len(c[s])> 0):
                denom = len(c[s])
            list_value_temp = sum(c[s])/ denom
            returnlist.append(list_value_temp)
    print ("returnlist")
    print (returnlist)
    print ("^returnlist")
    return returnlist








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
@user_passes_test(token_check, login_url='/demosky/verify-user/')
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
@user_passes_test(token_check, login_url='/demosky/verify-user/')
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
            Filter = request.POST.getlist('Filter')
            print(key)
            n=len(Filter)
            # for i in range(n):
            #     obj=lookup(Filter,i)
            #     print(obj)
            print(n)
            print(Filter)


            if key:
                if User.objects.filter(username=key).exists():
                    u = User.objects.get(username=(key))
                    args = {'user': u}
                    return render(request, 'demosky/search_profile.html', args)
                else:
                    if Filter:
                        if n == 1:
                            if ('bio_filter' in Filter):

                                SearchProfile = UserProfile.objects.filter(
                                    Q(bio__icontains=key)
                                )



                            if ('birthplace_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                    Q(birthplace__icontains=key)
                                    )


                            if ('work_filter'in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                    Q(work__icontains=key)
                                )


                            if ('location_filter'in Filter):

                                SearchProfile = UserProfile.objects.filter(
                                    Q(location__icontains=key)
                                    )
                        elif n == 2:
                            if ('bio_filter' in  Filter and 'location_filter' in Filter):
                                print("taking 2")
                                SearchProfile = UserProfile.objects.filter(
                                   Q(bio__icontains=key) |
                                   Q(location__icontains=key)
                               )
                                print(SearchProfile)

                            if ('bio_filter'in  Filter and 'birthplace_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                    Q(bio__icontains=key) |
                                    Q(birthplace__icontains=key)


                                )

                            if ('bio_filter' in  Filter  and 'work_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                    Q(bio__icontains=key) |
                                    Q(work__icontains=key)


                                )

                            if ('birthplace_filter' in  Filter  and 'location_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                    Q(location__icontains=key) |
                                    Q(birthplace__icontains=key)

                                )
                            if ('work_filter' in  Filter  and 'location_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(

                                    Q(location__icontains=key) |
                                    Q(work__icontains=key)


                                )
                            if ('birthplace_filter' in  Filter  and 'work_filter' in Filter):
                                print("reached here")
                                SearchProfile = UserProfile.objects.filter(

                                    Q(birthplace__icontains=key) |
                                    Q(work__icontains=key)

                                )
                        elif n == 3:
                            if ('bio_filter' in  Filter  and 'location_filter' in  Filter  and 'work_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                   Q(bio__icontains=key) |
                                   Q(location__icontains=key) |
                                   Q(work__icontains=key)

                               )
                            if ('bio_filter' in  Filter  and 'birthplace_filter' in  Filter  and 'location_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(
                                    Q(bio__icontains=key) |
                                    Q(birthplace__icontains=key) |
                                    Q(location__icontains=key)
                                )
                            if ('birthplace_filter' in  Filter  and 'work_filter' in  Filter  and 'location_filter' in Filter):
                                SearchProfile = UserProfile.objects.filter(

                                    Q(birthplace__icontains=key) |
                                    Q(work__icontains=key) |
                                    Q(location__icontains=key)
                                )
                        elif n == 4:
                            SearchProfile = UserProfile.objects.filter(
                                Q(bio__icontains=key) |
                                Q(location__icontains=key) |
                                Q(birthplace__icontains=key) |
                                Q(work__icontains=key) 
                            )

                    else:
                        SearchProfile = UserProfile.objects.filter(
                            Q(bio__icontains=key) |
                            Q(location__icontains=key) |
                            Q(quote__icontains=key) |
                            Q(birthplace__icontains=key) |
                            Q(work__icontains=key) |
                            Q(study__icontains=key) |
                            Q(fav_sen__icontains=key)

                        )

                    print(SearchProfile)
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
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def Chatbox(request):
    c = Chat.objects.filter(topic= '')
    return render(request, "demosky/chat_box.html", {'home': 'active', 'chat': c})

@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox',None)
        topicname = request.POST.get('topicname')

        # topic_name=request.POST.get('topic')
        print(msg)
        # print(topic_name)
        c = Chat(user=request.user, message=msg, topic=topicname)

        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def Messages(request):
    topicname = (request.GET.get('topicname'))
    c = Chat.objects.filter(topic = topicname)
    return render(request, 'demosky/messages.html', {'chat': c})


@login_required
@user_passes_test(token_check, login_url='/demosky/verify-user/')
def topic_edit(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if (action == 'add'):
            topic_var = request.POST.get('topic', None)
            print(topic_var)
            t= topics(topic=topic_var)
            if topic_var != '':
                 t.save()
            error = "Topic is added to discussion board successfully."
            topiclist = topics.objects.all()
            return render(request, 'demosky/topic_edit.html', {'topiclist':topiclist, 'error': error})

        if (action == 'delete'):
            print("Delete view")
            topic_select=request.POST.getlist('topiclist')
            if topic_select is not None:
                for topic_name in topic_select:
                    print(topic_name)
                    removetopic=topics.objects.get(topic=str(topic_name))
                    removetopic.delete()
                error = "Topic deleted successfully."
            else:
                error="No topic deleted."
            topiclist=topics.objects.all()
            return render(request, 'demosky/topic_edit.html', {'topiclist': topiclist, 'error': error})


        if (action == 'displaytopic'):
            topic_select = request.POST.get('topiclist')
            print(topic_select)
            c=Chat.objects.filter(topic = topic_select)
            return render(request,"demosky/chat_box.html",{'home': 'active', 'chat':c, 'topic':topic_select})


    else:
        topiclist = topics.objects.all()
        return render(request, 'demosky/topic_edit.html',{'topiclist':topiclist})


# def lookup(d,key):
#         return d[key]


##################################### end Shantanu##################################################