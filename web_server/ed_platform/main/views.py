from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.defaultfilters import title

from main.forms import LoginForm
from main.services import *
from templates import *

def test(request):
    #register('Sasha', '555', 'S')
    #register('Oleg', '123', 'S')
    #register('Sultan', '16k', 'T')

    #add_course('Proga', teacher_id=Users.objects.get(username='Sultan').id)
    #join_course(Users.objects.get(username='Oleg').id, Courses.objects.get(name='Proga').id)

    #add_material(Courses.objects.get(name='Proga').id,topic ='soft', name = 'C', text='lia lia lia bla bla bla')

    #add_comment(1, 'Good!')

    #add_grade(Users.objects.get(username = 'Oleg').id, Courses.objects.get(name='Proga').id, 5)

    #send_message(Users.objects.get(username = 'Oleg').id, Users.objects.get(username = 'Sasha').id, 'po pivu?')
    #send_message(Users.objects.get(username = 'Sasha').id, Users.objects.get(username = 'Oleg').id, 'go')
    #d = get_dialogue(Users.objects.get(username = 'Sasha').id, Users.objects.get(username = 'Oleg').id)
    #d = get_users_with_dialogues(Users.objects.get(username = 'Sasha').id)
    d = has_dialogue(Users.objects.get(username = 'Sasha').id, Users.objects.get(username = 'Oleg').id)

    return render(request, 'test.html', {"title" : "Test", "dialogue" : d})

'''
@login_required
def user_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('home')  # Перенаправление на домашнюю страницу
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form' : form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

'''