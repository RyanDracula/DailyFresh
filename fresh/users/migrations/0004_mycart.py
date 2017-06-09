# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('users', '0003_auto_20170602_2328'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('goods_id', models.ForeignKey(to='goods.GoodsInfo')),
                ('per_id', models.ForeignKey(to='users.UserInfo')),
            ],
        ),
    ]
