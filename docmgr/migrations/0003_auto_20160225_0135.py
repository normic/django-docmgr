# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('docmgr', '0002_auto_20151031_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='id',
        ),
        migrations.AddField(
            model_name='document',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=b'docmgr/2016', verbose_name='File'),
        ),
    ]
