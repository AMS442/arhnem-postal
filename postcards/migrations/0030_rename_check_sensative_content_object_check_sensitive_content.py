# Generated by Django 4.1.7 on 2023-11-09 16:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("postcards", "0029_remove_object_reason_for_return_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="object",
            old_name="check_sensative_content",
            new_name="check_sensitive_content",
        ),
    ]