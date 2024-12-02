
from django.contrib import admin
from django.urls import path
from main.views import *

from django.urls import path
from main.views import register_user, login_user

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('register/', registration, name='register'),
    #path('login/', user_login, name='login'),
    #path('', test),
    #path('', UsersFormView.as_view(), name="create_user"),
    #path('', users_form, name="create_user"),
    #path('', courses_form, name="create_courses"),
    path('register/', register_user, name="register_user"),
    path('login/', login_user, name="login_user"),
    path('', register_user, name="create_user"),
]
