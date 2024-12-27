from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
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
                "error": "Неверное имя пользователя или пароль.",
                "username": username
            })
    return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')

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
        tests = Test.objects.filter(course__in=courses).order_by('course__name')
        context = {
            'user': user,
            'courses': progress_data,
            'grades': grades,
            'materials': materials,
            'tests': tests,  # Оптимизация названия ключа
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
def view_courses(request):
    courses = Courses.objects.all()
    return render(request, 'view_courses.html', {'courses': courses})

@login_required
def apply_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    if request.method == 'POST':
        application, created = CourseApplication.objects.get_or_create(student=request.user, course=course)
        if created:
            application.save()
            return redirect('view_courses')
        else:
            return JsonResponse({'error': 'You have already applied to this course.'}, status=400)
    return render(request, 'apply_course.html', {'course': course})

@login_required
def manage_applications(request):
    if request.user.role != Users.TEACHER:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    applications = CourseApplication.objects.filter(course__teacher=request.user, status='PENDING')
    return render(request, 'manage_applications.html', {'applications': applications})

@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(CourseApplication, id=application_id)
    if request.user != application.course.teacher:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

@login_required
def update_application_status(request, application_id, status):
    # Приводим статус к верхнему регистру
    status = status.upper()
    application = get_object_or_404(CourseApplication, id=application_id)
    # Проверка, что текущий пользователь является преподавателем курса
    if request.user != application.course.teacher:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    # Обновление статуса заявки
    if status in ['ACCEPTED', 'REJECTED']:
        application.status = status
        application.save()
        if status == 'ACCEPTED':
            # Добавление студента к курсу
            application.course.students.add(application.student)
        return redirect('manage_applications')  # Перенаправление после успешного обновления
    # Если статус некорректен
    return JsonResponse({'error': 'Invalid status'}, status=400)


@login_required
def add_material_view(request, course_id):
    if request.user.role != 'T':  # Проверка, что пользователь преподаватель
        return HttpResponseForbidden("Только преподаватели могут добавлять материалы.")

    course = get_object_or_404(Courses, id=course_id, teacher=request.user)  # Проверяем, что курс принадлежит преподавателю

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course  # Устанавливаем курс автоматически
            material.save()
            return redirect('manage_courses')
    else:
        form = MaterialForm(initial={'course': course})  # Предзаполняем поле курс

    return render(request, 'add_course_materials.html', {'form': form, 'course': course})


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


from django.http import JsonResponse

@login_required
def create_test(request):
    if request.user.role != Users.TEACHER:  # Проверяем роль пользователя
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            # Сохраняем тест
            test = test_form.save(commit=False)
            test.teacher = request.user
            test.save()

            # Обработка вопросов
            question_texts = request.POST.getlist('question_text')  # Получаем список вопросов
            for i, question_text in enumerate(question_texts):
                if question_text.strip():  # Пропускаем пустые вопросы
                    # Создаём вопрос
                    question = Question.objects.create(test=test, text=question_text)

                    # Обработка вариантов ответов для текущего вопроса
                    choice_texts = request.POST.getlist(f'choice_text_{i}')  # Текст вариантов ответа
                    is_correct_keys = request.POST.getlist(f'is_correct_{i}')  # Список чекбоксов

                    for j, choice_text in enumerate(choice_texts):
                        if choice_text.strip():  # Пропускаем пустые варианты ответа
                            # Проверяем, является ли вариант правильным
                            is_correct = str(j) in is_correct_keys
                            Choice.objects.create(
                                question=question,
                                text=choice_text,
                                is_correct=is_correct
                            )

            return redirect('profile')  # Перенаправление после успешного создания теста

    else:
        test_form = TestForm()

    return render(request, 'create_test.html', {'test_form': test_form})






@login_required
def available_tests(request):
    if request.user.role != Users.STUDENT:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Получаем курсы, на которые записан студент
    enrolled_courses = Courses.objects.filter(students=request.user)
    # Получаем тесты для этих курсов
    tests = Test.objects.filter(course__in=enrolled_courses)

    return render(request, 'available_tests.html', {'tests': tests})

@login_required
def take_test(request, test_id):
    if request.user.role != Users.STUDENT:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    test = get_object_or_404(Test, id=test_id)

    # Проверяем, что студент записан на курс, связанный с тестом
    if not test.course.students.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'You are not enrolled in this course.'}, status=403)

    if request.method == 'POST':
        # Получаем ответы студента
        student_answers = request.POST.dict()
        correct_answers = 0
        total_questions = test.questions.count()

        for question in test.questions.all():
            # Получаем правильные ответы для вопроса
            correct_choices = question.choices.filter(is_correct=True)
            selected_choices = [
                int(choice_id) for key, choice_id in student_answers.items() if key.startswith(f'question_{question.id}')
            ]

            # Проверяем правильность ответов
            if set(correct_choices.values_list('id', flat=True)) == set(selected_choices):
                correct_answers += 1

        # Рассчитываем оценку (в процентах)
        grade = int((correct_answers / total_questions) * 100)

        # Сохраняем оценку в модели Grades
        Grades.objects.create(
            grade=grade,
            student=request.user,
            course=test.course
        )

        return render(request, 'test_result.html', {'grade': grade})

    return render(request, 'take_test.html', {'test': test})
