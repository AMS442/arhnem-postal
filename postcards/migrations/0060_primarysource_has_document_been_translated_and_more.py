# Generated by Django 4.2.11 on 2024-04-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0059_primarysource_cataloger_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="primarysource",
            name="has_document_been_translated",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="primarysource",
            name="number_of_pages",
            field=models.IntegerField(
                blank=True,
                help_text="How many pages does the document have?",
                null=True,
                verbose_name="Number of pages",
            ),
        ),
        migrations.AddField(
            model_name="primarysource",
            name="title",
            field=models.CharField(
                blank=True,
                help_text="Title of the document.",
                max_length=255,
                null=True,
                verbose_name="Title",
            ),
        ),
    ]
