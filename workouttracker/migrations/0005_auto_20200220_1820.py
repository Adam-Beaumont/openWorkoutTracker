# Generated by Django 2.1.1 on 2020-02-20 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouttracker', '0004_run'),
    ]

    operations = [
        migrations.RenameField(
            model_name='run',
            old_name='dateAdded',
            new_name='date',
        ),
    ]
