# Generated by Django 4.1.7 on 2023-11-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0028_alter_primarysource_related_postal_items"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="object",
            name="reason_for_return",
        ),
        migrations.AddField(
            model_name="object",
            name="reason_for_return_original",
            field=models.TextField(
                blank=True,
                help_text="The reason for return in the original language.",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="object",
            name="reason_for_return_translated",
            field=models.TextField(
                blank=True,
                help_text="The reason for return translated to English.",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="object",
            name="letter_type",
            field=models.CharField(
                choices=[
                    ("postcard", "Postcard"),
                    ("letter", "Letter"),
                    ("package", "Package"),
                    ("envelope", "Envelope"),
                    ("folded card", "Folded Card"),
                    ("envelope printed matter", "Envelope ('printed matter')"),
                    ("letter sheet", "Letter Sheet"),
                    ("giro envelope", "Giro Envelope"),
                    ('envelope ("printed matter")', 'Envelope ("printed matter")'),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="primarysource",
            name="person",
            field=models.ManyToManyField(
                blank=True,
                help_text="Select the person(s) this document is about. If the person does not exist, click the plus and add the new person.",
                related_name="person",
                to="postcards.person",
                verbose_name="person",
            ),
        ),
    ]
