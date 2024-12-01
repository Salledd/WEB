from django import forms
from main.models import *


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["username", "password", "role"]
        #widgets = {'username': forms.TextInput(attrs={})}


'''class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ["name", "description"]
        #widgets = {'username': forms.TextInput(attrs={})}'''