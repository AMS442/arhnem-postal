# Generated by Django 4.1.7 on 2023-11-02 13:54

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0021_alter_object_letter_enclosed"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="reasonreturn",
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="transcription",
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
