
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name="login_user"),
    path('profile/', profile_view, name='profile'),
    #path('login/', user_login, name='login'),
    path('', test, name='manage_courses'),
]
