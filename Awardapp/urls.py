from django.conf import settings
from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns =[
    path('',views.welcome,name='welcome'),
    path('register', views.register, name = 'register'),
    path('login',views.login,name = 'login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('accounts/',include('registration.backends.simple.urls')),
    path('post',views.post,name = 'post'),
    path('profile',views.profile,name= 'profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('project_details/<project_id>',views.project_details,name= 'project_details'),
    path('api/profiles',views.ProfileList.as_view()),
    path('api/posts',views.PostList.as_view())
    
]