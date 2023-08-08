from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone



UserModel = get_user_model()

class Topic(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(UserModel, through='UserTopicRelationship')

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255, default='default_title')
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE,  null=True)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.title

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author= models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
    

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"

        

class UserTopicRelationship(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    notify = models.BooleanField(default=False)
