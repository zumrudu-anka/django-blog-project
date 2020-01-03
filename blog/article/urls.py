from django.contrib import admin
from django.urls import path
from .views import *

app_name = "article"

urlpatterns = [
    path('dashboard/', dashboard, name = "dashboard"),
    path('addarticle/', addarticle, name = "addarticle"),
    path('update/<int:id>', updatearticle, name = "updatearticle"),
    path('delete/<int:id>', deletearticle, name = "deletearticle"),
]