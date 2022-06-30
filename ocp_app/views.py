
import re
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user_details, course_table, educator_table, enrolled_user
from .serializers import RegisterUserSerializer, LoginUserSerializer, CourseSerializer

logedIn = False
as_educator = False
logedInUser = user_details()

@api_view(['GET'])
def appOverview(request):
    api_urls = {
        'login': 'login/',
        'signup': 'signup/',
        'add course':'login/addCourse/',
        'list all courses':'login/listAll/', 
        'view course': 'login/viewCourse', 
        'enroll course':'login/listAll/enrollCourse', 
        'view enroled course':'login/viewEnroledUser'
    }
    return Response(api_urls)


@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        print(request.data)
        item = RegisterUserSerializer(data=request.data)
    
        # validating for already existing data
        if user_details.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
        if item.is_valid():
            item.save()
            return Response(item.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return HttpResponse("Only post method is allowed")        

@api_view(['POST'])
def loginUser(request):

    if request.method == 'POST':
        # item = LoginUserSerializer(data=request.data)
        print(request.data)
        if user_details.objects.filter(**request.data).exists():
            global logedInUser
            global logedIn
            logedInUser = user_details.objects.filter(**request.data)[0]
            logedIn = True
            if user_details.objects.filter(**request.data)[0].role == 'Educator':
                global as_educator
                as_educator = True
            return Response("You are succesfully logged in")
        else:
            return Response("Invalid credentials")    

@api_view(['POST'])
def addCourse(request):
    global logedIn
    global as_educator
    if logedIn and as_educator:
        if request.method == 'POST':
            item = CourseSerializer(data=request.data)
        
            # validating for already existing data
            if course_table.objects.filter(**request.data).exists():
                raise serializers.ValidationError('This data already exists')
            if item.is_valid():
                item.save()
                educatorCourse = educator_table()
                educatorCourse.course_id = course_table.objects.filter(**request.data)[0]
                educatorCourse.user_id = logedInUser
                educatorCourse.save()
                return Response(item.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("You need to login as educator to add a course")


@api_view(['GET'])
def listAllCourse(request):
    global logedIn
    global as_educator
    if logedIn and as_educator == False:
        if request.method == 'GET':
               allCourses = [i.course_name for i in course_table.objects.all()]
               return Response(allCourses)
        else:
            return HttpResponse("Only get method is allowed")
    else:
        return HttpResponse("You need to login as a learner to view all courses")               


@api_view(['POST'])
def viewCourse(request):
    global logedIn
    global as_educator
    if logedIn and as_educator == False:
        if request.method == 'POST':
            print(request.data)
            courseDetails = course_table.objects.filter(course_name = request.data['name'])
            if len(courseDetails):
                return Response({
                    "name": courseDetails[0].course_name,
                    "course_description": courseDetails[0].course_description
                })
            else:
                return HttpResponse('Invalid course name')  
        else:
            return HttpResponse('Only POST method is allowed')
    else:
        return HttpResponse("You need to login as a learner to view a course")        

@api_view(['POST'])
def enrollCourse(request):
    global logedIn
    global as_educator
    if logedIn and as_educator == False:
        if request.method == 'POST':
            global logedInUser
            courseDetails = course_table.objects.filter(course_name = request.data['name'])
            
            if len(courseDetails) and len(enrolled_user.objects.filter(
                    
                    course_id = courseDetails[0],
                    user_id = logedInUser 
                
                ).all()) == 0:
                enrolledUser = enrolled_user()
                enrolledUser.course_id = courseDetails[0]
                enrolledUser.user_id = logedInUser
                
                enrolledUser.save()
                return Response({
                    
                    "course_name": courseDetails[0].course_name,
                    "enrolled_user": logedInUser.user_name,
                    "message": "successfull enrolled" 
                
                })
            else:
                return HttpResponse("Already enrolled")
        else:
            return HttpResponse('Only post method is allowed')
    else:
        return HttpResponse("Please login as a learner to enroll in a course")                    

@api_view(['POST'])
def viewEnroledUsers(request):
    global logedIn
    global as_educator

    if logedIn and as_educator:
        if request.method == 'POST':
            courseDetails = course_table.objects.filter(course_name = request.data['name'])
            if len(courseDetails):
                hasCreated = educator_table.objects.filter(course_id = courseDetails[0], user_id = logedInUser)
                if len(hasCreated) > 0:
                    allUsers = enrolled_user.objects.filter(course_id = courseDetails)
                    return HttpResponse(allUsers)
                else:
                    return HttpResponse("Unauthorised access! You can only view users of a course created by you")
            else:
                return HttpResponse("Invalid course name")
        else:
            return HttpResponse("Only post method is allowed")
    else:
        return HttpResponse("You need to login as an educator")

            