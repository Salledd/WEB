from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.defaultfilters import title

from main.forms import *
from main.services import *
from templates import *

def test(request):
    #register('Sasha', '555', 'S')
    #register('Oleg', '123', 'S')
    #register('Sultan', '16k', 'T')
    #register('Kostya', 'parol', 'S')
    #add_course('Dota', 'from Golovach')
    #join_course(get_id_user('Kostya'), Courses.objects.get(name = 'Dota'))
    #send_message(get_id_user('Kostya'), get_id_user('Oleg'), 'go v dotu')
    #add_course('Matan', teacher=Users.objects.get(username='Lomov'))
    #join_course(Users.objects.get(username='Oleg').id, Courses.objects.get(name='Proga').id)

    #add_material(Courses.objects.get(name='Proga').id,topic ='soft', name = 'C', text='lia lia lia bla bla bla')

    #add_comment(1, 'Good!')

    #add_grade(Users.objects.get(username = 'Oleg').id, Courses.objects.get(name='Proga').id, 5)

    #send_message(Users.objects.get(username = 'Oleg').id, Users.objects.get(username = 'Sasha').id, 'po pivu?')
    #send_message(Users.objects.get(username = 'Sasha').id, Users.objects.get(username = 'Oleg').id, 'go')
    d = get_dialogue(Users.objects.get(username = 'Kostya'), Users.objects.get(username = 'Oleg'))
    #d = get_users_with_dialogues(Users.objects.get(username = 'Sasha').id)
    #d = has_dialogue(Users.objects.get(username = 'Sasha').id, Users.objects.get(username = 'Oleg').id)

    return render(request, 'test.html', {"title" : "Test", "test_v" : Users.objects.get(username = 'Oleg').courses_set.all()})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = register(username=cleaned_data['username'],
                password=cleaned_data['password'],
                role=cleaned_data['role'])
            # логирование действия
            UserLog.objects.create(user=user, action="Создание пользователя")

            login(request, user)    # автоматический вход после регистрации
            return redirect('profile')  # Перенаправление после успешной регистрации
        else:
            return render(request, 'registration.html', {
                "form": form,
                "error": form.errors
            })
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {"form": form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # логирование действия
            UserLog.objects.create(user=user, action="Вход пользователя")
            return redirect('profile')
            #return render(request, 'test.html', {"title" : "Test", "test_v" : request.user.username})  # перенаправление после успешного входа
        else:
            return render(request, 'login.html', {
                "error": "Неверное имя пользователя или пароль."
            })
    return render(request, 'login.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Courses, Grades, Materials, Progress


@login_required
def profile_view(request):
    user = request.user

    if user.role == 'S':  # Если студент
        courses = user.courses_set.all()
        progress_data = []
        for course in courses:
            progress = Progress.objects.filter(student=user, course=course).first()
            progress_percentage = progress.progress_percentage if progress else 0
            progress_data.append({
                'name': course.name,
                'progress_percentage': progress_percentage
            })
        grades = Grades.objects.filter(student=user)
        materials = Materials.objects.filter(course__in=courses)

        context = {
            'user': user,
            'courses': progress_data,
            'grades': grades,
            'materials': materials,
        }

    elif user.role == 'T':  # Если преподаватель
        courses = Courses.objects.filter(teacher=user)
        performance = Grades.objects.filter(course__in=courses).values('student', 'course').annotate(
            average_grade=models.Avg('grade')
        )

        context = {
            'user': user,
            'courses': courses,
            'performance': performance,
        }

    else:
        context = {'user': user}  # Для неопределенной роли

    return render(request, 'profile.html', context)


#def profile_student(request):
#    return render(request, 'profile_student.html', {"user" : request.user, "courses" : request.user.courses_set.all()})

#def profile_teacher(request):
#    return render(request, 'profile_teacher.html', {"user" : request.user, })