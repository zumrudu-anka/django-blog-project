from django.contrib import admin
from django.urls import path
from .views import *
app_name = "article"

urlpatterns = [
    path('create/', index, name = "index"),
]