# Generated by Django 5.1.1 on 2024-11-23 19:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0014_alter_forum_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resources',
            name='dateuploaded',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
