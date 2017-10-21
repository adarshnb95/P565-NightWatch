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
from django.http import HttpResponse, HttpResponseRedirect
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



# Create your views here.
def test():
    pass
    a = Sensors.objects.all()
    bundle = {}
    for j in a:
        bundle[int(j.sensor_id)] = [str(j.sensor_id),j.x_coord,j.y_coord,str(j.img_name),j.light_data,j.battery_level]
    #print bundle
    return bundle


# Create your views here.
def home(request):
    full_list = json.dumps(test())
    light_list = json.dumps(ldat())
    print light_list
    return render(request,'demosky/home.html',{'full_list':full_list , 'light_list':light_list})

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


def profile(request):
    args = {'user': request.user}
    return render(request, 'demosky/profile.html', args)


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
def verify(request):
    if request.method == 'POST':
        print (request.POST)
        token = request.POST.get('token')
        forms = request.POST.get('tokenform')       
        newEmailUser = UserProfile.objects.get(user=request.user)
        print (newEmailUser.token)
        print (token)
        if(int(token) == int(newEmailUser.token)):
            print("Great Success")
            return render(request,'demosky/home.html')
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

