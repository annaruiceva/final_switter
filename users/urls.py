from django.urls import path, include
from django.views.generic import TemplateView

from users import views
from users.views import profile

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='registration/invalid_verify.html'),
        name='invalid_verify'
    ),
    path(
        'verify_email/<uidb64>/<token>/',
        views.EmailVerify.as_view(),
        name='verify_email',
    ),
    path(
        'email_confirm/',
        TemplateView.as_view(template_name='registration/email_confirm.html'),
        name='email_confirm'),

    path('register/', views.Register.as_view(), name='register'),
    path('<user_name>/', views.profile, name='profile'),
    path('prof/<name>/', views.profile, name='profile2'),

]
