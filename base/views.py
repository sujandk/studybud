from django.shortcuts import render

# Create your views here.

rooms = [
    {'id' : 1 , 'name': 'Lets learn python'},
    {'id' : 2 , 'name': 'Design with me'},
    {'id' : 3 , 'name': 'Frontend developers'},
]

def home(request):
    contex = {'rooms' : rooms }
    return render(request , 'base/home.html' , contex)

def room(request , pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i['name']
    context = {'room' : room  }
    return render(request , 'base/room.html' , context)