# Generated by Django 5.1.2 on 2024-12-01 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0023_researchpub_dept_name_researchpub_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researchpub',
            old_name='article_website',
            new_name='article_site',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='name_of_authors',
            new_name='authors_name',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='is_listed_in_ugc_care',
            new_name='is_ugc_care',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='issn_number',
            new_name='issn_no',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='name_of_journal',
            new_name='jrnl_name',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='journal_website',
            new_name='jrnl_site',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='title_of_paper',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='researchpub',
            old_name='year_of_publication',
            new_name='yr_of_pub',
        ),
    ]
