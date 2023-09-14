# Generated by Django 4.2.5 on 2023-09-14 11:48

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
                ('profile_bio', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_link', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_link', models.CharField(blank=True, max_length=100, null=True)),
                ('follows', models.ManyToManyField(blank=True, related_name='follow_by', to='accounts.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]