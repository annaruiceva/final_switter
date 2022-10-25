from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_img/%Y/%m/%d/', default='user_img/1.jpg', blank=True)
    status = models.CharField(max_length=30, blank=True)
    about = models.CharField(max_length=200, blank=True)

    friends = models.ManyToManyField("Profile", blank=True)
    subs = models.ManyToManyField("Profile", blank=True, related_name="%(class)s_subs")

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Twitts(models.Model):
    # create_date = models.DateTimeField(auto_now_add=True)
    # для FAKER
    create_date = models.DateTimeField()

    text = RichTextField(max_length=300)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    likes = models.ManyToManyField('Profile', blank=True, related_name='likes')
    dislikes = models.ManyToManyField('Profile', blank=True, related_name='dislikes')

    def __str__(self):
        return self.text


@receiver(signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('create profile, sender: ', sender)
    if created:
        print('created', instance)
        Profile.objects.create(
            user=instance,
        )
    print('create_profile, **kwargs: ', kwargs)


class Comment(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    twitt = models.ForeignKey('Twitts', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.twitt)
