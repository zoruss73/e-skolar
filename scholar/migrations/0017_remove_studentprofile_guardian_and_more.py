# Generated by Django 5.2 on 2025-05-01 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scholar', '0016_alter_studentprofile_birth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='guardian',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='guardian_address',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='guardian_no',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='rel_in_guardian',
        ),
    ]
