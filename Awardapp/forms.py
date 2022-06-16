from django import forms
from django.contrib.auth.forms import UserCreationForm
from django. contrib.auth.models import User
from .models import *
class NewUserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']
        
class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_photo','contact']
        
        
class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','contact','profile_photo']
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design_rate','usability_rate',"content_rate",]
    

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description','url','image','title']        