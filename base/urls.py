from django.urls import path
from . import views 

urlpatterns = [
    path('login/' , views.loginPage , name ='loginPage'),
    path('logoutUser/' , views.logoutUser , name ='logoutUser'),
    path('register/' , views.registerPage , name ='registerPage'),
    path('' , views.home , name ='home'),
    path('room/<str:pk>' , views.room , name= 'room'),

    path('createRoom/' , views.createRoom , name= 'createRoom'),
    path('updateRoom/<str:pk>' , views.updateRoom , name='updateRoom'),
    path('deleteRoom/<str:pk>' , views.deleteRoom , name='deleteRoom')
]