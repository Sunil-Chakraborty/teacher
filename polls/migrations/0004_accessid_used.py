# Generated by Django 5.1.2 on 2025-03-05 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_remove_accessid_used_alter_accessid_access_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessid',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
