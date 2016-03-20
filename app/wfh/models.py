from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Word(models.Model):
    # 目前最长的英文单词有45个字母
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

class Article(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    words = models.ManyToManyField(Word)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.user.username
