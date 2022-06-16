from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',)
        profile_photo = CloudinaryField('profile_photo')
        bio = models.TextField(max_length=100,blank=True)
        contact = models.EmailField(blank=True, max_length=100)

        def __str__(self):
                return self.contact

        def update(self):
                self.save()    
        
        def delete_profile(self):
                self.delete()
@classmethod
def get_profile_by_user(cls, searched_term):
        profile = cls.objects.filter(name__icontains=searched_term)
        return profile 
        
        
class Post(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='post',)
        image = CloudinaryField('profile_photo')
        url = models.URLField(max_length=100,blank=True)
        description= models.TextField(max_length=100,blank=True)
        contact = models.EmailField(blank=True, max_length=100)
        title = models.CharField(blank=True,max_length=100)
        
        def __str__(self):
                return self.contact

        def update(self):
                self.save()    
        
        def delete_post(self):
                self.post()
@classmethod
def get_post_by_user(cls, searched_term):
        post = cls.objects.filter(name__icontains=searched_term)
        return post 
        
class Rating(models.Model):
        user = models.ForeignKey(User,on_delete=models.CASCADE)
        post = models.ForeignKey(Post,on_delete=models.CASCADE)
        design_rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0)
        usability_rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0)
        content_rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0)
        average_score = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0)

        def __str__(self):
                return f'{self.post}'        