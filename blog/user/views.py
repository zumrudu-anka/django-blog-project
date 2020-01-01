from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import *
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request,newUser)
        return render(request,"index.html")
    context = {
        'form': form
    }
    return render(request, "register.html", context)

def loginUser(request):
    return render(request, "login.html")
def logoutUser(request):
    pass