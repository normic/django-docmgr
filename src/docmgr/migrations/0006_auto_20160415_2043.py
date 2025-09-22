# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('docmgr', '0005_auto_20160409_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(help_text='Click on fieldname or image to open the upload dialog.', storage=django.core.files.storage.FileSystemStorage(location=b'kittdocmgr/'), upload_to=b''),
        ),
    ]
