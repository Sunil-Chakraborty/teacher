# Generated by Django 5.1.2 on 2025-03-05 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_faculty_id_votingsession_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accessid',
            name='used',
        ),
        migrations.AlterField(
            model_name='accessid',
            name='access_id',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
