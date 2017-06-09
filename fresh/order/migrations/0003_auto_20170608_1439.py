# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20170608_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='user',
            new_name='goods',
        ),
    ]
