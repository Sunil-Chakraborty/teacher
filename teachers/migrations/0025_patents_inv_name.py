# Generated by Django 5.1.2 on 2024-12-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0024_rename_article_website_researchpub_article_site_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patents',
            name='inv_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Name of the Inventors'),
        ),
    ]