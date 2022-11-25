# Generated by Django 4.0.2 on 2022-11-25 14:07

import django.contrib.auth.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='UUID Field')),
                ('username', models.CharField(default=uuid.uuid4, editable=False, max_length=100, unique=True, verbose_name='Username')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email address')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Last name')),
                ('patronymic', models.CharField(blank=True, max_length=30, null=True, verbose_name='Patronymic')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Is superuser')),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatars', verbose_name='Avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
