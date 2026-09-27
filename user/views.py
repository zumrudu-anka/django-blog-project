from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from blog.ratelimit import ratelimit
from .forms import *

User = get_user_model()


def _next_url(request):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts = {request.get_host()}):
        return next_url
    return "index"


@ratelimit("register", limit = 10, period = 60 * 60)
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.success(request, "Aramıza hoş geldin, {}!".format(username))
        return redirect("index")
    return render(request, "register.html", {"form": form})


@ratelimit("login", limit = 10, period = 60 * 5)
def loginUser(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username = username, password = password)
        if user is None:
            messages.error(request, "Kullanıcı adı veya parola hatalı.")
        else:
            login(request, user)
            messages.success(request, "Tekrar hoş geldin, {}!".format(user.username))
            return redirect(_next_url(request))
    return render(request, "login.html", {"form": form})


@require_POST
def logoutUser(request):
    logout(request)
    messages.info(request, "Çıkış yaptınız.")
    return redirect("index")
