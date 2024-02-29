# Generated by Django 4.2.10 on 2024-02-29 16:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0054_censor_censor_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="object",
            options={
                "ordering": ["-date_of_correspondence"],
                "verbose_name": "Postal Material",
                "verbose_name_plural": "Postal Materials",
            },
        ),
        migrations.RemoveField(
            model_name="object",
            name="related_images",
        ),
        migrations.RemoveField(
            model_name="primarysource",
            name="related_postal_items",
        ),
    ]
