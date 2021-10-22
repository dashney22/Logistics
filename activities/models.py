from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('share-thoughts')

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(blank= True, null= True)
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default="Philosophy")
    likes = models.ManyToManyField(User, related_name="blog_likes")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('share-thoughts')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return '%s - %s' %(self.post.title, self.name)
