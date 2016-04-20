# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import docmgr.models


class Migration(migrations.Migration):

    dependencies = [
        ('docmgr', '0007_auto_20160415_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=docmgr.models.get_upload_path, storage=django.core.files.storage.FileSystemStorage(location=b'c:/dev/venvs/kitt/kitt/files/docmgr'), verbose_name='Document File'),
        ),
    ]
