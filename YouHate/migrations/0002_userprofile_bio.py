# Generated by Django 2.2.28 on 2025-03-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YouHate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default='This user has no bio.'),
        ),
    ]
