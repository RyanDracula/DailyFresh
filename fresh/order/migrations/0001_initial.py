# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('users', '0004_mycart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('odate', models.DateTimeField(auto_now_add=True)),
                ('oIsPay', models.BooleanField(default=False)),
                ('ototal', models.DecimalField(max_digits=6, decimal_places=2)),
                ('oaddress', models.ForeignKey(to='users.AdrressInfo')),
                ('user', models.ForeignKey(to='users.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='order.OrderInfo'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='user',
            field=models.ForeignKey(to='goods.GoodsInfo'),
        ),
    ]
