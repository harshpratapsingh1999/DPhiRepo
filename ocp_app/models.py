from operator import mod
from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
class user_details(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.TextField(max_length=50, unique=True)
    role = models.TextField(max_length=10)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)


class course_table(models.Model):
    course_id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=100, unique=True)
    course_description = models.TextField(max_length=200)
    course_content = models.TextField(max_length=1000)


class educator_table(models.Model):
    user_id = models.ForeignKey(user_details, on_delete=models.CASCADE)
    course_id = models.ForeignKey(course_table, on_delete=models.CASCADE)


class enrolled_user(models.Model):
    user_id = models.ForeignKey(user_details, on_delete=models.CASCADE)
    course_id = models.ForeignKey(course_table, on_delete=models.CASCADE)

