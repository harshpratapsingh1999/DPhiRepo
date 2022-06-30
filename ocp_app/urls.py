from unicodedata import name
from django.urls import path
from . import views
  
urlpatterns = [
    path('', views.appOverview, name='home'),
    path('signup/', views.registerUser, name='signup'),
    path('login/', views.loginUser, name='login'),
    path('login/addCourse/', views.addCourse, name='addCourse'),
    path('login/listAll/', views.listAllCourse, name='listAllCourses'),
    path('login/viewCourse', views.viewCourse, name='viewCourse'),
    path('login/listAll/enrollCourse', views.enrollCourse, name='enrollCourse'),
    path('login/viewEnroledUsers', views.viewEnroledUsers, name="viewEnroledUsers")
]