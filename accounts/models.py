from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='follow_by', symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    profile_bio = models.CharField(max_length=500, null=True, blank=True)
    facebook_link = models.CharField(max_length=100, null=True, blank=True)
    instagram_link = models.CharField(max_length=100, null=True, blank=True)
    linkedin_link = models.CharField(max_length=100, null=True, blank=True)


# @receiver(post_save, sender=User)
# def create_profile(instance, create, **kwargs):
#     if create:
#         user_profile = Profile(user=instance)
#         user_profile.save()
#         user_profile.follows.set([instance.profile.id])
#         user_profile.save()

# post_save.connect(create_profile, sender=User) -----> this method or receiver decorator
