# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('docmgr', '0003_auto_20160225_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(help_text='An optional description of the file', verbose_name='Description', blank=True),
        ),
    ]
