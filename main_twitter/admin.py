from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from main_twitter.models import Profile, Twitts

User = get_user_model()
admin.site.register(Profile)


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("username", "email", "is_active", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    actions = ('deactivate', 'activate_user')


@admin.register(Twitts)
class TwittsAdmin(admin.ModelAdmin):
    pass
