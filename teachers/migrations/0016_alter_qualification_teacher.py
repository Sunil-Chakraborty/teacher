# Generated by Django 5.1.2 on 2024-11-27 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0015_delete_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher'),
        ),
    ]