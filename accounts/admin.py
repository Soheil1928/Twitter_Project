from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile


admin.site.unregister(Group)
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    filter_horizontal = ['follows']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'is_active', 'is_superuser']
    list_display = ['id', 'username', 'is_active']
    list_editable = ['is_active']
    inlines = [ProfileInline]
