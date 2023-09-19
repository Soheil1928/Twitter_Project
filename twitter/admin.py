from django.contrib import admin
from .models import Tweet, Tag


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'create_at']
    filter_horizontal = ['like']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
