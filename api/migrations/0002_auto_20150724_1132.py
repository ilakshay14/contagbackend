# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BlockedList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('by_user', models.ForeignKey(to='api.User')),
                ('for_user', models.ForeignKey(related_name='blocked_user', to='api.User')),
            ],
        ),
        migrations.CreateModel(
            name='OTPToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('contact_number', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=55)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to='api.User')),
            ],
        ),
        migrations.DeleteModel(
            name='ProfileRequest',
        ),
        migrations.AddField(
            model_name='adminplatform',
            name='is_binary',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_muted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='group_type',
            field=models.ForeignKey(default=1, to='api.AdminGroup'),
        ),
    ]
