from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={}),
            'password': forms.PasswordInput(attrs={}),
        }



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['receiver', 'text']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),  # Виджет для выбора получателя
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите сообщение...'}),
        }
        labels = {
            'receiver': 'Получатель',
            'text': 'Сообщение',
        }

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)  # Получаем отправителя из переданных параметров
        super().__init__(*args, **kwargs)

        # Ограничиваем список получателей (например, исключаем самого отправителя)
        if sender:
            self.fields['receiver'].queryset = Users.objects.exclude(id = sender.id)
