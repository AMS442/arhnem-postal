# Generated by Django 4.1.7 on 2024-01-23 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0051_alter_image_historical_source"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="historical_source",
        ),
        migrations.AddField(
            model_name="primarysource",
            name="file",
            field=models.ForeignKey(
                blank=True,
                help_text="Upload images of the document.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="postcards.image",
                verbose_name="Upload images",
            ),
        ),
    ]
