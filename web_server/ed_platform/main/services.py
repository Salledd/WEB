from main.models import *


def get_id_user(username : str):
    return Users.objects.get(username=username).id

def register(username : str, password : str, role : chr):
    user = Users.objects.create_user(username=username, password=password, role =role)
    return user

def add_course(name, description = None, teacher : Users = None):
    if teacher is None:
        teacher_id = None
    else:
        teacher_id = teacher.id
    Courses.objects.create(name = name, description = description, teacher_id = teacher_id)

def add_material(course_id, topic, name, text = None, pdf = None, photo = None, video = None, link = None):
    course = Courses.objects.get(id = course_id)
    material = Materials(topic = topic, name = name, text = text, pdf = pdf, photo = photo, video = video, link = link)
    material.save()
    course.materials_set.add(material)

def join_course(student : Users, course_id):
    course = Courses.objects.get(id = course_id)
    course.students.add(student)

def del_student_from_course(student : Users, course_id):
    course = Courses.objects.get(id = course_id)
    course.students.remove(student)

def add_comment(material_id, comment_text : str):
    comment = Comments(text = comment_text)
    comment.save()
    material = Materials.objects.get(id = material_id)
    material.comments_set.add(comment)

def del_comment(comment_id):
    comment = Comments.objects.get(id = comment_id)
    comment.delete()

def add_grade(student : Users, course_id, mark : int):
    course = Courses.objects.get(id = course_id)
    grade = Grades(grade = mark)
    grade.save()
    student.grades_set.add(grade)
    course.grades_set.add(grade)

def send_message(sender : Users, receiver : Users, text_message : str):
    if sender == receiver:
        raise ValueError("Нельзя отправить сообщение самому себе.")
    if not text_message.strip():
        raise ValueError("Сообщение не может быть пустым.")
    message = Messages.objects.create(
        sender=sender,
        receiver=receiver,
        text=text_message,
    )

def get_users_with_dialogues(user : Users):
    """
    Возвращает список пользователей, с которыми у данного пользователя есть переписка
    :param user: Пользователь, для которого нужно найти собеседников
    :return: QuerySet пользователей
    """
    from django.db.models import Q
    # Получаем всех пользователей, участвующих в переписке с данным пользователем
    users = Users.objects.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct()

    return users

def get_dialogue(user1 : Users, user2 : Users):
    """
    Возвращает список сообщений между двумя пользователями, отсортированный по времени
    :param user1: Первый пользователь
    :param user2: Второй пользователь
    :return: QuerySet сообщений
    """

    messages = Messages.objects.filter(
        sender=user1, receiver=user2
        ) | Messages.objects.filter(
        sender=user2, receiver=user1
        ).order_by('timestamp')
    return messages

def has_dialogue(user1 : Users, user2 : Users):
    """
    Проверяет, есть ли переписка между двумя пользователями
    :return: True, если переписка существует, иначе False
    """

    from django.db.models import Q
    return Messages.objects.filter(
        (models.Q(sender=user1, receiver=user2) |
         models.Q(sender=user2, receiver=user1))
    ).exists()

