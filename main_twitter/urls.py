"""djangoTwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main_twitter import views

urlpatterns = [
    path('fake/users', views.fake_create_user, name='create_users'),
    path('fake/twitts', views.fake_create_twitts, name='create_twitts'),

    path('create_post/', views.create_twitt, name="create_post"),
    path('search_people/', views.show_people, name="search_people"),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),
    path("<str:username>/subs", views.profile_subs, name='profile_subs'),
    path("<str:username>/friends", views.profile_friends, name='profile_friends'),
    path("settings/<str:username>", views.settings, name='settings'),
    path("change_info/", views.change_info, name='change_info'),
    path('delete/<int:pk>', views.delete_twitt, name='delete_twitt'),
    path('<int:pk>/like/', views.AddLike.as_view(), name='like'),
    path('<int:pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
    path('comments/<int:pk>/', views.show_comments, name='comments'),
    path('create_comment/<int:pk>/', views.create_comment, name='create_comment'),

    # path('', include('main_twitter.urls'))

]
