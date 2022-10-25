from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from main_twitter.models import Profile, Twitts, Comment

User = get_user_model()


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("username", "email", "is_active", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    actions = ('deactivate', 'activate_user')
    #
    # @admin.display(description='image')
    # def user_avatar(self, twitt: Twitts):
    #     return Profile.objects.get(user_id=twitt.author.id).image

@admin.register(Twitts)
class TwittsAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    # list_display = ("user_id", "text", "image", "create_date")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
