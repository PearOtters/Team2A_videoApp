# Generated by Django 2.2.28 on 2025-03-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YouHate', '0004_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/profile_pictures/defaultPfp.jpg', upload_to='profile_pictures/'),
        ),
    ]
