from email import message
from webbrowser import get
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Room,Topic
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# rooms=[
#     {'id': 1,'name':"Let's learn Python"},
#     {'id': 2,'name':"Design with me"},
#     {'id': 3,'name':"Frontend Developers"}
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect("base:home")
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, r"User does not exist")
        user= authenticate(request, username=username, password=password)    
        
        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, r"Username or Password is incorrect!")
        
       
    context={'page':page}
    return render(request,'base/login.html',context)
    
    # stopped at 2:35

def logoutUser(request):
    logout(request)
    return redirect('base:home')

def registerUser(request):
    page='register'
    form=UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('base:home')
        else:
            messages.error(request, 'An error occured during registration')
    context={
        'form':form,
        'page':page
    }
    return render(request,'base/login.html', context)

def homepage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
         Q(name__icontains=q)   |
         Q(description__icontains=q)|
         Q(host__username__icontains=q))
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-updated')

    context={'rooms':rooms,
             'topics':topics,
             'room_count':room_count,
             'room_messages':room_messages}
    return render(request, 'base/home.html', context)
    

def pagerooms(request, pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('created')
    participants=room.participants.all()
    if request.method=='POST':
        message= Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('base:rooms', pk=room.id)

    context={'room':room,
            'room_messages':room_messages,
            'participants':participants
            }
    return render(request, 'base/room.html',context)

@login_required(login_url='base:loginpage')
def createRoom(request):
    form=RoomForm()
    if request.method== "POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render (request, "base/room_form.html",context)


@login_required(login_url='base:loginpage')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user!= room.host:
        return HttpResponse('You are not allowed to edit this room')

    if request.method== "POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='base:loginpage')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room')

    if request.method == "POST":
        room.delete()
        return redirect('/')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='base:loginpage')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')

    if request.method == "POST":
        message.delete()
        return redirect('base:home')

    return render(request,'base/delete.html',{'obj':message})