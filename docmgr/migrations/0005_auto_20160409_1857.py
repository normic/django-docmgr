# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import docmgr.models


class Migration(migrations.Migration):

    dependencies = [
        ('docmgr', '0004_auto_20160228_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(help_text='An optional description of the file.', verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(help_text='Click on fieldname or image to open the upload dialog.', upload_to=docmgr.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='document',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
