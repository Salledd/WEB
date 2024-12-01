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
    teacher_id = models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Materials(models.Model):
    topic = models.CharField(max_length=128)
    name = models.CharField(max_length=128, blank=False)
    text = models.TextField(null=True)
    pdf = models.FileField(null=True)
    photo = models.ImageField(null=True)
    video = models.FileField(null=True)
    link = models.TextField(null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Comments(models.Model):
    text = models.TextField()
    material = models.ForeignKey(Materials, on_delete=models.CASCADE, null=True)

class Grades(models.Model):
    grade = models.IntegerField()
    student = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.grade

class Messages(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, default=None, related_name='sent_messages', )
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE,default=None, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.Now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['timestamp']  # для сортировки по времени

