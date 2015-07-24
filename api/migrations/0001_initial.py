# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPlatform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform_name', models.CharField(max_length=255)),
                ('is_api_available', models.BooleanField(default=False)),
                ('sync_type', models.CharField(default=b'link', max_length=55, choices=[(b'api', b'Platform API'), (b'link', b'Link to platform profile'), (b'handle', b'Handle or username')])),
                ('priority', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('contact_name', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=255, null=True)),
                ('is_on_contag', models.BooleanField(default=False)),
                ('is_invited', models.BooleanField(default=False)),
                ('invited_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('platform_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('is_public', models.BooleanField(default=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PushNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('contag', models.CharField(max_length=8)),
                ('mobile_number', models.CharField(max_length=100)),
                ('landline_number', models.CharField(max_length=100, null=True)),
                ('emergency_contact_number', models.CharField(max_length=100, null=True)),
                ('is_mobile_verified', models.BooleanField(default=False)),
                ('gender', models.CharField(default=b'f', max_length=1)),
                ('personal_email', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=500)),
                ('work_email', models.CharField(max_length=255, null=True)),
                ('work_mobile_number', models.CharField(max_length=100, null=True)),
                ('work_landline_number', models.CharField(max_length=100, null=True)),
                ('work_address', models.CharField(max_length=100, null=True)),
                ('website', models.CharField(max_length=100, null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('work_facebook_page', models.CharField(max_length=100, null=True)),
                ('android_app_link', models.CharField(max_length=100, null=True)),
                ('ios_app_link', models.CharField(max_length=100, null=True)),
                ('avatar_url', models.CharField(max_length=500)),
                ('blood_group', models.CharField(max_length=55)),
                ('date_of_birth', models.DateField()),
                ('marital_status', models.BooleanField(default=False)),
                ('marriage_anniversary', models.DateField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('interest', models.CharField(max_length=255)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to='api.User')),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_contag_user',
            field=models.ForeignKey(related_name='Contag_Contact', to='api.User', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
    ]
