# Generated by Django 5.1.2 on 2024-11-22 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_teacher_first_name_alter_teacher_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='dept_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
