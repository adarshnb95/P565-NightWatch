from django.shortcuts import redirect


def login_redirect(request):
	return redirect('/demosky/login')


def base_page(request):
	return redirect('/demosky/homebasic')