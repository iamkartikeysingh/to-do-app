# Generated by Django 4.2.1 on 2023-09-30 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
