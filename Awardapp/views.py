from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.http.response import HttpResponseRedirect
from Awardapp.forms import *
from django.contrib.auth.forms import UserCreationForm
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,PostSerializer
from Awardapp import serializer
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def welcome(request):
    post = Post.objects.all()
    return render(request,'index.html',{'posts':post})

def register(request):
    form = NewUserform()
    
    if request.method == 'POST':
        form = NewUserform(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'register.html',{'form':form})
    
def login(request):
    return render(request, 'login.html')
    
def logout(request):
    return render(request, 'login.html')    
    
@login_required(login_url="/accounts/login/")    
def profile(request):
    if request.method == 'POST':
        form = UserProfile(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form = UserProfile()
    return render(request,'profile.html', {'form':form})
    
@login_required(login_url='/accounts/login/')    
def editprofile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            profile = Profile(user=request.user)
            profile.save()
            form.save()
            return redirect('profile')
    else:
        form = EditProfile()
    return render(request,'profile.html', {'form':form})

@login_required(login_url="/accounts/login/")
def post(request):
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES)
        print (form.errors)
        print(form.is_valid)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = (request.user)
            post.save()
            return redirect('welcome')
        return render(request, 'post.html', {'form': form})
    else:
        
        form =ProjectsForm()
        return render(request, 'post.html', {'form': form})



def project_details(request, project_id):
    form = RatingForm()
    current_user = request.user
    all_ratings = Rating.objects.filter(post=project_id).all()
    post = Post.objects.filter(pk = project_id)
    ratings = Rating.objects.filter(user=request.user,post=project_id).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(project=project_id)
#calculating design
            design_ratings = [design.design_rating for design in post_ratings]
            design_rating_average = sum(design_ratings) / len(design_ratings)
#calculating content
            content_ratings = [content.content_rating for content in post_ratings]
            content_rating_average = sum(content_ratings) / len(content_ratings)
#calculating usability
            usability_ratings = [usability.usability_rating for usability in post_ratings]
            usability_rating_average = sum(usability_ratings) / len(usability_ratings)
#calculating average
            aggregate_average_rate = (design_rating_average + usability_rating_average + content_rating_average) / 3
            print(aggregate_average_rate)
            rate.design_rating_average = round(design_rating_average, 2)
            rate.usability_rating_average = round(usability_rating_average, 2)
            rate.content_rating_average = round(content_rating_average, 2)
            rate.aggregate_average_rate = round(aggregate_average_rate, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
        return render(request, 'projectdetails.html', {'current_user':current_user,'all_ratings':all_ratings,'post':post,'rating_form': form,'rating_status': rating_status})
    
    
class ProfileList(APIView):
    def get(self,request,format=None):
        profiles = Profile.objects.all()
        serializers = ProfileSerializer(profiles,many = True)
        return Response(serializers.data)
        
        
class PostList(APIView):
    def get(self,request,format=None):
        posts = Post.objects.all()
        serializers = PostSerializer(posts,many = True)
        return Response(serializers.data)        