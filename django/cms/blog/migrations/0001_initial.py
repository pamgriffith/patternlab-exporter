# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.SlugField()),
                ('excerpt', markupfield.fields.MarkupField(rendered_field=True)),
                ('excerpt_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, choices=[(b'', b'--'), (b'markdown', b'markdown')])),
                ('content', markupfield.fields.MarkupField(rendered_field=True)),
                ('_excerpt_rendered', models.TextField(editable=False)),
                ('content_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, choices=[(b'', b'--'), (b'markdown', b'markdown')])),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('_content_rendered', models.TextField(editable=False)),
            ],
        ),
    ]
