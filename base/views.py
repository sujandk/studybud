from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators  import login_required
from .models import Room , Topic 
from django.contrib.auth.models import User
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# rooms = [
#     {'id' : 1 , 'name': 'Lets learn python'},
#     {'id' : 2 , 'name': 'Design with me'},
#     {'id' : 3 , 'name': 'Frontend developers'},
# ]




def loginPage(request):
    page = 'login'
    context = {'page' : page}
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request , username =  username , password = password)

        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")

    return render(request , 'base/login_register.html' , context )

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context = {'form'  : form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'An error occured during registeration')

    return render(request , 'base/login_register.html' , context)

def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q ) |
        Q(name__icontains = q ) |
        Q(description__icontains = q ))
    topics = Topic.objects.all()
    room_counts = rooms.count()
    contex = {'rooms' : rooms  , 'topics': topics , 'rooms_counts' : room_counts}
    return render(request , 'base/home.html' , contex)

def room(request , pk):
    room = Room.objects.get(id = pk)
    context = {'room' : room}
    return render(request , 'base/room.html' , context)


@login_required(login_url= 'loginPage')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect('home')
    context = {'form' : form}
    return render(request, 'base/createRoom.html' , context )

@login_required(login_url= 'loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/createRoom.html' , context)

@login_required(login_url= 'loginPage')
def deleteRoom(request , pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request , 'base/delete.html' , {'obj': room})