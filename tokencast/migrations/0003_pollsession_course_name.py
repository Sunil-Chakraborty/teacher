# Generated by Django 5.1.2 on 2025-03-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokencast', '0002_pollsession_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollsession',
            name='course_name',
            field=models.CharField(default=1234, max_length=255),
            preserve_default=False,
        ),
    ]
