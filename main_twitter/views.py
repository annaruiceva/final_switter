from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View

from main_twitter import models
from main_twitter.forms import CreatePostForm, UpdateUserForm, UpdateProfileForm, CreateCommentForm
from main_twitter.models import Twitts, Profile
from faker import Faker

User = get_user_model()

def fake_create_user(request):
    f = Faker('ru-RU')
    for i in range(10):
        print(i)
        p = f.profile()
        User.objects.create(
            username=p['username'],
            email=p['mail'],
            password=f.password(length=8)
        )
    return redirect('/')


def fake_create_twitts(request):
    f = Faker('ru-RU')
    profiles = Profile.objects.all()
    for p in profiles:
        models.Twitts.objects.bulk_create(
            [
                models.Twitts(
                    text=f.sentence(nb_words=5),
                    create_date=f.date_time_between(),
                    author=p
                ) for _ in range(10)
            ]
        )
        print(p.user.username)
    return redirect('/')

def show_home_twitt(request):
    info = {"twitts": list(models.Twitts.objects.all().order_by('-create_date'))}
    print(info)
    return render(request, 'main_twitter/home.html', info)


def show_comments(request, pk):
    twitt = Twitts.objects.get(pk=pk)
    print(twitt.pk)
    info = {"twitt": twitt}
    info['comments'] = list(models.Comment.objects.all().filter(twitt=info['twitt']))

    print(info)
    return render(request, 'main_twitter/comment.html', info)


def create_comment(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CreateCommentForm(request.POST)
            twitt = models.Twitts.objects.get(id=pk)
            if comment_form.is_valid():
                # user_profile = User.objects.all().get(username=request.user.username).profile
                # comment = user_profile.comment_set.create(
                #     text=request.POST["text"])
                # user_profile.save()
                # comment.save()
                new_comment = comment_form.save(commit=False)
                new_comment.twitt = twitt
                new_comment.author = request.user.profile
                new_comment.save()
            else:
                comment_form = CreateCommentForm()
    return redirect('comments', pk)


# class TwittDeleteView(LoginRequiredMixin, DeleteView):
#     model = models.Twitts
#     success_url = '/profile'
# friend = User.objects.all().get(username=username)
# user = request.user
#
# user.profile.friends.remove(friend.profile)
# user.profile.save()
# friend.profile.subs.remove(user.profile)
# friend.profile.save()
def delete_twitt(request, pk):
    if request.method == 'POST':
        # if request.user.is_authenticated and request.user.username == models.Twitts.objects.get(id=pk).author:
        try:
            models.Twitts.objects.get(id=pk).delete()
            return redirect('profile', request.user.username)
        except models.Twitts.DoesNotExist:
            return HttpResponseNotFound(request)

    else:
        return HttpResponseNotAllowed(request)


def create_twitt(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = CreatePostForm(request.POST)
            if user_form.is_valid():
                user = User.objects.all().get(username=request.user.username).profile
                profile = user.twitts_set.create(
                    text=request.POST["text"])
                user.save()
                profile.save()
    return redirect('profile', request.user.username)


def show_people(request):
    user_name = request.user.username
    # print('-----------')
    # print(user_name)
    # print('-----------')
    info = {
        "user": User.objects.all().get(username=user_name),
        "search_str": request.GET.get('s', '')
    }
    q_people = models.Profile.objects.filter(~Q(user__username=user_name)).order_by('user__username')
    info["friends"] = info["user"].profile.friends.all()
    info["friends_name"] = info["user"].profile.friends.all().values_list('user__username', flat=True)
    # print(q_people.query)
    print(request.GET.get('s'))

    if request.GET.get('s'):
        print(request.GET.get('s'))
        s = request.GET['s']
        q_people = models.Profile.objects.filter(~Q(user__username=user_name) & Q(user__username__contains=s)).order_by(
            'user__username')

    else:
        q_people = models.Profile.objects.filter(~Q(user__username=user_name)).order_by('user__username')
    info['people'] = q_people

    print(info)

    return render(request, 'main_twitter/search.html', info)


def add_friend(request, username):
    print(username)
    if request.user.is_authenticated:
        friend = User.objects.all().get(username=username)
        user = User.objects.all().get(username=request.user.username)
        user.profile.friends.add(friend.profile)
        user.profile.save()
        friend.profile.subs.add(user.profile)
        friend.profile.save()
        print(request.META.get('HTTP_REFERER'))
        if 'search_people' in str(request.META.get('HTTP_REFERER')):
            return redirect('search_people')
        return redirect('profile', username)
    return redirect('home')


def remove_friend(request, username):
    if request.user.is_authenticated:
        friend = User.objects.all().get(username=username)
        user = request.user

        user.profile.friends.remove(friend.profile)
        user.profile.save()
        friend.profile.subs.remove(user.profile)
        friend.profile.save()
    return redirect('profile', username)


def profile_friends(request, username):
    user = User.objects.all().get(username=username)
    info = {
        "friends": user.profile.friends.all(),
        "title": "Подписки @" + username
    }

    return render(request, 'main_twitter/profile_friends.html', info)


def profile_subs(request, username):
    user = User.objects.all().get(username=username)
    info = {
        "friends": user.profile.subs.all(),
        "title": "Подписчики @" + username
    }
    print(info)
    return render(request, 'main_twitter/profile_friends.html', info)


def settings(request, username):
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)

    info = {
        "user": User.objects.all().get(username=username),
        "own": False,
        'user_form': user_form,
        'profile_form': profile_form
    }
    if request.user.is_authenticated and request.user.username == username:
        info["own"] = True
    return render(request, 'main_twitter/change_info.html', info)


@transaction.atomic
def change_info(request):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        #     new_username = request.POST["new_username"]
        #     if User.objects.filter(username=new_username).exists():
        #         return render(request, 'main_twitter/change_info.html',
        #                       {'error': f'User with \'{new_username}\' username already exists'})
        #     user = User.objects.all().get(username=request.user.username)
        #     user.username = new_username
        #     user.save()
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                print('valid--------')
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect('profile', request.user.username)
        else:
            print('invalid--------')
            messages.success(request, 'Your profile is not updated')

        return render(request, 'main_twitter/change_info.html', {'user_form': user_form, 'profile_form': profile_form})


class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        twitt = Twitts.objects.get(pk=pk)
        user = twitt.author.user.username

        profile = request.user.profile
        is_dislike = False

        for dislike in twitt.dislikes.all():
            if dislike == profile:
                is_dislike = True
                break

        if is_dislike:
            twitt.dislikes.remove(profile)

        is_like = False

        for like in twitt.likes.all():
            if like == profile:
                is_like = True
                break

        if not is_like:
            twitt.likes.add(profile)

        if is_like:
            twitt.likes.remove(profile)

        if str(request.META.get('HTTP_REFERER')).count('/') == 3:
            return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(reverse('profile', args=[user]))


class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        twitt = Twitts.objects.get(pk=pk)
        user = twitt.author.user.username
        print(user, twitt.author, '-----------------')

        profile = request.user.profile

        is_like = False

        for like in twitt.likes.all():
            if like == profile:
                is_like = True
                break

        if is_like:
            twitt.likes.remove(profile)

        is_dislike = False

        for dislike in twitt.dislikes.all():
            if dislike == profile:
                is_dislike = True
                break

        if not is_dislike:
            twitt.dislikes.add(profile)

        if is_dislike:
            twitt.dislikes.remove(profile)
        if str(request.META.get('HTTP_REFERER')).count('/') == 3:
            return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(reverse('profile', args=[user]))




