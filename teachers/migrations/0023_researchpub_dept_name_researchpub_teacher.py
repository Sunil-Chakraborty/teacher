# Generated by Django 5.1.2 on 2024-12-01 03:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0022_researchpub_created_date_researchpub_updated_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchpub',
            name='dept_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='researchpub',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher'),
        ),
    ]
