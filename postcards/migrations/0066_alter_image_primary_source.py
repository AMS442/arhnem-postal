# Generated by Django 4.2.11 on 2024-04-24 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0065_image_primary_source_alter_image_postcard_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="primary_source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="postcards.primarysource",
            ),
        ),
    ]
