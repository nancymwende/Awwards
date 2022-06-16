from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.http.response import HttpResponseRedirect
from Awardapp.forms import *
from django.contrib.auth.forms import UserCreationForm
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,PostSerializer
from django.contrib.auth.models import User


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
    
def profile(request):
    if request.method == 'POST':
        form = UserProfile(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('index')
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
    
# def projectform(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST,request.FILES,instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProjectForm()
#     return render(request,'project.html', {'form':form})

def post(request):
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.user = request.User
            projects.save()
        return redirect('index')
    else:
        form =ProjectsForm(request.POST)
    return render(request, 'post.html', {'form': form})


# def post(request):
#     current_user = request.user
#     profiles = Profile.objects.all()
#     for profile in profiles:
#         if profile.user.id == current_user.id:
#             if request.method == 'POST':
#                 form = ProjectsForm(request.POST,request.FILES)
#                 if form.is_valid():
#                     upload = form.save(commit=False)
#                     upload.posted_by = current_user
#                     upload.profile = profile
#                     upload.save()
#                     return redirect('index')
#             else:
#                 form = ProjectsForm()
#             return render(request,'post.html',{"form":form})
def project_details(request, project_id):
    form = RatingForm()
    current_user = request.user
    all_ratings = Rating.objects.filter(post=project_id).all()
    post = Post.objects.get(pk = project_id)
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