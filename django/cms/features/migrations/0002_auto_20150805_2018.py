# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='img_alt',
            field=models.CharField(default='Default image', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feature',
            name='img_src',
            field=models.ImageField(default='features/default.png', upload_to=b'features'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feature',
            name='url',
            field=models.SlugField(),
        ),
    ]
