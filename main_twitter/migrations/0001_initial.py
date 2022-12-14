# Generated by Django 4.1.1 on 2022-10-14 20:46

from django.conf import settings
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
                ('status', models.CharField(blank=True, max_length=30)),
                ('about', models.CharField(blank=True, max_length=200)),
                ('friends', models.ManyToManyField(blank=True, to='main_twitter.profile')),
                ('subs', models.ManyToManyField(blank=True, related_name='%(class)s_subs', to='main_twitter.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
