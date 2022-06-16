from django.urls import path
from . import views

urlpatterns =[
    path('',views.welcome,name='welcome'),
    path('register', views.register, name = 'register'),
    path('login',views.login,name = 'login'),
    path('post',views.post,name = 'post'),
    path('profile',views.profile,name= 'profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('project_details/<project_id>',views.project_details,name= 'project_details'),
    path('api/profiles',views.ProfileList.as_view()),
    path('api/posts',views.PostList.as_view())
    
]