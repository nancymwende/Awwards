from django.shortcuts import render,redirect
from django.http  import HttpResponse
from Awardapp.forms import NewUserform,UserProfile,EditProfile
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def welcome(request):
    return render(request,'index.html')

def register(request):
    form = NewUserform()
    
    if request.method == 'POST':
        form = NewUserform(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'register.html',{'form':form})
    
def login(request):
    return render(request, 'login.html')    
    
def profile(request):
    if request.method == 'POST':
        form = UserProfile(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfile()
    return render(request,'profile.html', {'form':form})
    
def editprofile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfile()
    return render(request,'profile.html', {'form':form})    