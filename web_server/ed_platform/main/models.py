from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import datetime


class Users(AbstractUser):
    STUDENT = 'S'
    TEACHER = 'T'
    ROLES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    role = models.CharField(choices=ROLES, max_length=1, default=STUDENT)
    def __str__(self):
        return self.username

class Courses(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(null=True)
    students = models.ManyToManyField(Users)
    teacher = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': Users.TEACHER}, related_name='teacher')
    def __str__(self):
        return self.name

class Materials(models.Model):
    topic = models.CharField(max_length=128)
    name = models.CharField(max_length=128, blank=False)
    text = models.TextField(null=True, blank=True)
    pdf = models.FileField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    video = models.FileField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Comments(models.Model):
    text = models.TextField()
    material = models.ForeignKey(Materials, on_delete=models.CASCADE, null=True)

class Grades(models.Model):
    grade = models.IntegerField(null=True, blank=True)
    student = models.ForeignKey(Users, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    time_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_add']  # для сортировки по времени

    def __str__(self):
        return f"{self.student.username} - {self.course.name}: {self.grade}"


class Messages(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, default=None, related_name='sent_messages', )
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE,default=None, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.Now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['timestamp']  # для сортировки по времени

class UserLog(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    action = models.CharField(max_length=255)   # наше действие(создание)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.action} - {self.timestamp}"

class Progress(models.Model):
    student = models.ForeignKey(Users, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    completed_materials = models.ManyToManyField(Materials, blank=True)
    progress_percentage = models.FloatField(default=0.0)

    def update_progress(self):
        total = self.course.materials_set.count()
        completed = self.completed_materials.count()
        self.progress_percentage = (completed / total * 100) if total > 0 else 0
        self.save()


class Test(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE, limit_choices_to={'role': Users.TEACHER})
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='tests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    OPEN_ENDED = 'OE'
    MULTIPLE_CHOICE = 'MC'
    QUESTION_TYPES = [
        (OPEN_ENDED, 'Open-ended'),
        (MULTIPLE_CHOICE, 'Multiple-choice'),
    ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=2)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
