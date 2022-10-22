from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
# Create your views here.
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from main_twitter import models
from main_twitter.views import settings
from users.forms import UserCreationForm
from users.utils import send_email_for_verify
from django.contrib.auth.tokens import default_token_generator as token_generator

User = get_user_model()


def profile2(request, user_name):
    try:
        print('-----')

        user_profile = models.Profile.objects.get(user__username=user_name)
        print('-----', user_profile)

        return render(
            request,
            'registration/profile.html',
            {
                'profile': user_profile,

            }
        )
    except (User.DoesNotExist, models.Profile.DoesNotExist):
        return redirect('home')


def profile(request, user_name):
    # print(request.META.get('HTTP_REFERER'))
    info = {
        "cur_user": User.objects.all().get(username=user_name),
        "own": False,
        "twitts": [],
        "about": "",
        "friends": [],
        "friends_num": "0"
    }
    info["auth"] = request.user.is_authenticated
    info["twitts"] = list(info["cur_user"].profile.twitts_set.all().order_by('-create_date'))

    info["friends"] = info["cur_user"].profile.friends.all()
    info["friends_num"] = str(len(info["friends"]))

    info["subs"] = info["cur_user"].profile.subs.all()
    info["subs_num"] = str(len(info["subs"]))
    info["about"] = info["cur_user"].profile.about
    info["status"] = info["cur_user"].profile.status

    if request.user.is_authenticated and request.user.username == user_name:
        info["own"] = True
    else:
        info["sub"] = False
        for fr in request.user.profile.friends.all():
            if fr.user.username == user_name:
                info["sub"] = True
    # print(info)
    return render(request, 'registration/profile.html', info)


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError,
               User.DoesNotExist, ValidationError):
            user = None
        return user
        # if user is not None and default_token_generator.check_token(user, token):
        #     user.is_active = True
        #     user.save()
        #     return HttpResponse('Спасибо, что подтвердили регистрацию, теперь вы можете зайти на сайт')
        # else:
        #     return HttpResponse('Ссылка активации аккаунта неверна!')


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            send_email_for_verify(request, user)
            return redirect('email_confirm')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
#
#
# def profile(request, username):
#     """
#     Shows profile page
#
#     :param request: Django request object
#     :param username: Username whose page we are showing
#     :return: Django HttpResponse object
#     """
#     ctx = {
#         "user": User.objects.all().get(username=username),
#         "own": False,
#         "posts": [],
#         "bio": "",
#         "friends": [],
#         "friends_num": "0"
#     }
#     ctx["auth"] = request.user.is_authenticated
#     ctx["posts"] = list(
#         sorted(ctx["user"].profile.post_set.all(), reverse=True, key=lambda x: x.date))
#
#     ctx["friends"] = ctx["user"].profile.friends.all()
#     ctx["friends_num"] = str(len(ctx["friends"]))
#
#     ctx["subs"] = ctx["user"].profile.subs.all()
#     ctx["subs_num"] = str(len(ctx["subs"]))
#     ctx["bio"] = ctx["user"].profile.bio
#
#     if request.user.is_authenticated and request.user.username == username:
#         ctx["own"] = True
#     else:
#         ctx["sub"] = False
#         for fr in request.user.profile.friends.all():
#             if fr.user.username == username:
#                 ctx["sub"] = True
#     return render(request, 'registration/profile.html', ctx)
