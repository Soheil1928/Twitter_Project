from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_tweet = models.TextField()
    create_at = models.DateTimeField(auto_now=True)
    image_tweet = models.ImageField(blank=True, null=True, upload_to='tweet_images/')
    like = models.ManyToManyField(User, related_name='tweet_like')
    is_archive = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', related_name='tags_post', blank=True)

    def number_like(self):
        return self.like.count()

    def __str__(self):
        return f'{self.user}-({self.create_at: %Y-%m-%d %H:%M})'


class Tag(models.Model):
    tag_word = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.tag_word
