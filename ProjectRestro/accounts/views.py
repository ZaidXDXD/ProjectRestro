from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .decorators import unauthenticated_user
from .forms import (
    SignUpForm,
    ProfileForm
)

@unauthenticated_user
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form' : form})

@unauthenticated_user
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.filter(email=username.lower()).first()
        if user is not None:
            if user.check_password(raw_password=password):
                auth_login(request, user)
                return redirect('menuPage') 
            else:
                messages.info(request, "Please Check Your Usename And Password They Were Incorrect!")
        else:
            messages.info(request, "Please Check Your Usename And Password They Were Incorrect!")    
    return render(request, 'accounts/login.html')



def logoutuser(request):
    logout(request)
    return redirect('login')



@login_required(login_url = "login")
def profilepage(request):
    customer = request.user.profile
    form = ProfileForm(instance=customer)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'accounts/set_profile.html', context)
