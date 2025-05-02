from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 



class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    student_id = models.CharField(max_length=30, unique=True)
class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    teacher = models.CharField(max_length=100)

    def __str__(self):
         return f"{self.name} - {self.user.username}"

class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment_title = models.CharField(max_length=100)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.course.name} - {self.assignment_title}"

class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
    
    
    
# api/models.py

class CSESkillDevelopmentCourse(models.Model):
    
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name

