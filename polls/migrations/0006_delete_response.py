# Generated by Django 5.1.2 on 2025-03-06 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_feedback'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Response',
        ),
    ]
