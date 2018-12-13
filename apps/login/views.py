from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'login/index.html')

def create(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], pw_hash=hash1.decode('utf-8'))
        request.session['user_id'] = User.objects.get(id=user.id).id
        return redirect('/success')

def login(request):
    errors = User.objects.login(request.POST)
    print(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['login_email']).id
        return redirect('/success')

def success(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user,
    }
    print(user.first_name)
    return render(request, 'login/success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
