from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f'Category : {self.name}'

    # return to home when new category is added
    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=125)
    # content = models.TextField()
    content = RichTextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # post categories
    category = models.CharField(max_length=35, default='uncategorized')

    # likes
    likes = models.ManyToManyField(User, related_name='blog_posts')

    # get number of likes for a post

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Title : {self.title} || Author : {self.author.username}'

    # get absolute method for submission of new post from create post view
    # send submitted form where?
    def get_absolute_url(self):
        return reverse('home')

        # detail page of added post
        # return reverse('detail', args=[str(self.pk)])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by : {self.name} Comment : {self.body}'
