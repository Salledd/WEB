
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('register/', registration, name='register'),
    #path('login/', user_login, name='login'),
    path('', test),
]
