from django.urls import path
from . import views

urlpatterns =[
    path('',views.welcome,name='welcome'),
    path('register', views.register, name = 'register'),
    path('login',views.login,name = 'login'),
    path('profile',views.profile,name= 'profile'),
    path('editprofile',views.editprofile,name='editprofilre'),
    path('api/profiles',views.ProfileList.as_view()),
    path('api/posts',views.PostList.as_view())
]