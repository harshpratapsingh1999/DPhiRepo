from pyexpat import model
from statistics import mode
from django.db.models import fields
from rest_framework import serializers
from .models import user_details, course_table
  
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_details
        fields = "__all__"



class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_details
        fields = ('email', 'password')



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = course_table
        fields = "__all__"


