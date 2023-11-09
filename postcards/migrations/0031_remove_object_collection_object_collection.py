# Generated by Django 4.1.7 on 2023-11-09 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "postcards",
            "0030_rename_check_sensative_content_object_check_sensitive_content",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="object",
            name="collection",
        ),
        migrations.AddField(
            model_name="object",
            name="collection",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="postcards.collection",
                verbose_name="collection",
            ),
        ),
    ]
