# Generated by Django 4.2.10 on 2024-03-12 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "postcards",
            "0055_alter_object_options_remove_object_related_images_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="object",
            name="addressee_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="addressee_objects",
                to="postcards.person",
                verbose_name="addressee's name",
            ),
        ),
        migrations.AlterField(
            model_name="object",
            name="sender_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender_objects",
                to="postcards.person",
                verbose_name="sender's name",
            ),
        ),
        migrations.AlterField(
            model_name="transcription",
            name="postal_object",
            field=models.ForeignKey(
                blank=True,
                help_text="Link a document to the transcription.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="postcards.object",
            ),
        ),
    ]
