# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdrressInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.CharField(max_length=20)),
                ('addr', models.CharField(max_length=150)),
                ('youbian', models.CharField(max_length=8)),
                ('tel', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='adrressinfo',
            name='user',
            field=models.ForeignKey(to='users.UserInfo'),
        ),
    ]
