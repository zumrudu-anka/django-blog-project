from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('register/', register, name = "register"),
    path('login/', loginUser, name = "login"),
    path('logout/', logoutUser, name = "logout"),
    path('settings/', editProfile, name = "settings"),
    path('profile/<str:username>/', profile, name = "profile"),
]
