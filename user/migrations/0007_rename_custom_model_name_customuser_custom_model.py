# Generated by Django 5.1.2 on 2024-12-17 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_alter_customuser_model_selection_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="custom_model_name",
            new_name="custom_model",
        ),
    ]