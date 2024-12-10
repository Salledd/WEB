from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
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
    #d = get_dialogue(Users.objects.get(username = 'Kostya'), Users.objects.get(username = 'Oleg'))
    #d = get_users_with_dialogues(Users.objects.get(username = 'Sasha').id)
    #d = has_dialogue(Users.objects.get(username = 'Sasha').id, Users.objects.get(username = 'Oleg').id)

    return render(request, 'test.html', )


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

@login_required
def profile_view(request):
    user = request.user

    if user.role == 'S':  # Если студент
        courses = user.courses_set.all().order_by('name')
        progress_data = []
        for course in courses:
            progress = Progress.objects.filter(student=user, course=course).first()
            progress_percentage = progress.progress_percentage if progress else 0
            progress_data.append({
                'course': course,
                'name': course.name,
                'progress_percentage': progress_percentage
            })
        grades = Grades.objects.filter(student=user).order_by('course__name')
        materials = Materials.objects.filter(course__in=courses)

        context = {
            'user': user,
            'courses': progress_data,
            'grades': grades,
            'materials': materials,
        }

    elif user.role == 'T':  # Если преподаватель
        courses = Courses.objects.filter(teacher=user).order_by('name')

        performance = Grades.objects.filter(course__in=courses).select_related('student', 'course').values(
            'student__username', 'course__name'
        ).annotate(average_grade=models.Avg('grade')).order_by('course__name', 'student__username')

        context = {
            'user': user,
            'courses': courses,
            'performance': performance,
        }

    else:
        context = {'user': user}  # Для неопределенной роли

    return render(request, 'profile.html', context)


@login_required
def manage_courses_view(request):
    if request.user.role != 'T':  # Проверка, что пользователь преподаватель
        return HttpResponseForbidden("Только преподаватели могут управлять курсами.")

    courses = Courses.objects.filter(teacher=request.user)
    form_data = {}

    if request.method == 'POST':
        for course in courses:
            for student in course.students.all():
                form = GradeForm(request.POST, prefix=f"grade_{course.id}_{student.id}")
                if form.is_valid():
                    grade = form.cleaned_data['grade']
                    if grade is not None:  # Если поле оценки заполнено
                        # Создаем новую запись для оценки
                        Grades.objects.create(
                            student=student,
                            course=course,
                            grade=grade
                        )
        return redirect('manage_courses')

    for course in courses:
        form_data[course] = []
        for student in course.students.all():
            # Создаем пустую форму, без начального значения
            form = GradeForm(prefix=f"grade_{course.id}_{student.id}")
            form_data[course].append({'student': student, 'form': form})

    return render(request, 'manage_courses.html', {'courses': courses, 'form_data': form_data})


@login_required
def create_course_view(request):
    # Проверяем, что пользователь преподаватель
    if request.user.role != 'T':
        return HttpResponseForbidden("Только преподаватели могут создавать курсы.")

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('manage_courses')
    else:
        form = CourseForm()

    return render(request, 'create_course.html', {'form': form})

@login_required
def add_material_view(request):
    # Проверяем, что пользователь преподаватель
    if request.user.role != 'T':
        return HttpResponseForbidden("Только преподаватели могут добавлять материалы.")

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = MaterialForm()

    return render(request, 'add_course_materials.html', {'form': form})

@login_required
def add_student_to_course_view(request):
    if request.user.role != 'T':  # Проверка, что пользователь — преподаватель
        return HttpResponseForbidden("Только преподаватели могут добавлять студентов.")

    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            if course.teacher_id == request.user.id:  # Проверяем, что курс принадлежит преподавателю
                course.students.add(student)
                return redirect('manage_courses')
            else:
                return HttpResponseForbidden("Вы можете добавлять студентов только в свои курсы.")
    else:
        form = AddStudentForm()

    return render(request, 'add_student.html', {'form': form})

@login_required
def remove_student_from_course_view(request, course_id, student_id):
    if request.user.role != 'T':  # Проверка, что пользователь — преподаватель
        return HttpResponseForbidden("Только преподаватели могут удалять студентов.")

    course = get_object_or_404(Courses, id=course_id, teacher_id=request.user.id)
    student = get_object_or_404(Users, id=student_id, role='S')
    course.students.remove(student)
    return redirect('manage_courses')

def course_materials_view(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    materials = Materials.objects.filter(course=course)  # Фильтруем материалы по курсу
    return render(request, 'course_material.html', {'course': course, 'materials': materials})
