import imp
from django.urls import re_path,path,reverse
from . import views
from django.http import HttpResponse

app_name="base"

urlpatterns = [

    path('',views.homepage, name="homepage"),
    path('home/',views.homepage, name="home"),
    path('rooms/<str:pk>/',views.pagerooms, name="rooms"),
    path('create-room/',views.createRoom,name='createRoom'),
    path('update-room/<str:pk>/',views.updateRoom,name='updateRoom'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='deleteRoom'),
    path('login/',views.loginPage, name="loginpage"),
    path('register/',views.registerUser, name="register"),
    path('logout/',views.logoutUser, name="logout"),
    path('delete-message/<str:pk>/',views.deleteMessage,name='deletemessage'),


]
