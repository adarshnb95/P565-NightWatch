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




# Create your views here.
def home(request):
	return render(request,'demosky/home.html')


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/demosky')
		else:
			return redirect('/demosky/reg_form.html')	
	else:
		form = UserCreationForm()		
		args = {'form' : form}
		return render(request, 'demosky/reg_form.html', args)


def profile(request):
	args = {'user' : request.user}
	return render(request, 'demosky/profile.html', args)



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