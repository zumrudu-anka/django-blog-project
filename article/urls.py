from django.contrib import admin
from django.urls import path
from .views import *

app_name = "article"

urlpatterns = [
    path('', articles, name = "articles"),
    path('dashboard/', dashboard, name = "dashboard"),
    path('addarticle/', addarticle, name = "addarticle"),
    path('detail/<int:id>', detail, name = "detail"),
    path('update/<int:id>', updateArticle, name = "updateArticle"),
    path('delete/<int:id>', deleteArticle, name = "deleteArticle"),
    path('comment/<int:id>', comment, name = "comment"),

]