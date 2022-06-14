from dataclasses import fields
from rest_framework import serializers

from Awardapp.models import Post
from .models import Profile,Post


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =('bio','profile_photo','contact')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ('image','title','description','url')