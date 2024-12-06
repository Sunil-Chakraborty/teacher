# Generated by Django 5.1.2 on 2024-11-29 06:38

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0020_department_prog_cd'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAdmitted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Department Name')),
                ('prog_cd', models.CharField(blank=True, max_length=20, null=True, verbose_name='Programme Code')),
                ('acad_year', models.CharField(blank=True, max_length=9, null=True, validators=[django.core.validators.RegexValidator('^\\d{4}(/\\d{4})?$', "Enter a valid academic year (e.g., '2023' or '2023/2024').")], verbose_name='Academic Year')),
                ('sanc_seats', models.IntegerField(default=0, verbose_name='Number of Sanctioned Seats')),
                ('admit_seats', models.IntegerField(default=0, verbose_name='Number of Admitted Students')),
                ('reserv_catg', models.CharField(blank=True, choices=[('', 'Select Category'), (1, 'SC'), (2, 'ST'), (3, 'OBC-A'), (4, 'OBC-B'), (5, 'GEN')], max_length=7, null=True, verbose_name='Reserved Category Students')),
                ('seats_resrv_catg', models.IntegerField(default=0, verbose_name='Number of Reserved Category Students')),
                ('prog_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.department', verbose_name='Programme Name')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher', verbose_name='Assigned Teacher')),
            ],
        ),
    ]
