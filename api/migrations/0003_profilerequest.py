# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150724_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('request_type', models.CharField(max_length=255)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('for_user', models.ForeignKey(to='api.User')),
                ('to_user', models.ForeignKey(related_name='requested_user', to='api.User')),
            ],
        ),
    ]
