from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import *
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        messages.success(request,"Başarıyla Kayıt Oldunuz!")
        login(request,newUser)
        return redirect("index")
    context = {
        'form': form
    }
    return render(request, "register.html", context)

def loginUser(request):
    form  = LoginForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if user is None:
            messages.warning(request, "Kullanıcı Adı veya Parola Hatalı")
            context = {
                "form" : form
            }
            return render(request, "login.html", context)
        messages.success(request,"Başarıyla Giriş Yaptınız!")
        login(request, user)
        return redirect("index")
    context = {
        "form" : form
    }
    return render(request, "login.html", context)
def logoutUser(request):
    logout(request)
    messages.info(request,"Başarıyla Çıkış Yaptınız!")
    return redirect("index")