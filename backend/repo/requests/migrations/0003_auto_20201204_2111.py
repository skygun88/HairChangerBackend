# Generated by Django 3.1.3 on 2020-12-04 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_auto_20201204_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestinfo',
            name='convertedPath',
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='facePath',
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='hairPath',
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='requestinfo',
            name='rid',
        ),
    ]
